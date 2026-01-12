#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Set up any project based local script variables.
SCRIPT_NAME=$(basename -- "${BASH_SOURCE[0]}")
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
TEMP_FILE=$(mktemp /tmp/"${SCRIPT_NAME}".XXXXXXXXX)
TEMP_FILE2=$(mktemp ./"${SCRIPT_NAME}".XXXXXXXXX.txt)

SCRIPT_TITLE="Analyzing project dependencies"

# Perform any cleanup required by the script.
# shellcheck disable=SC2329
cleanup_function() {

	if [[ ${VERBOSE_MODE} -ne 0 ]]; then
		echo "{Performing clean up for script '${SCRIPT_NAME}'.}"
	fi

	# If the temp file was used, get rid of it.
	if [ -f "${TEMP_FILE}" ]; then
		rm "${TEMP_FILE}"
	fi
	if [ -f "${TEMP_FILE2}" ]; then
		rm "${TEMP_FILE2}"
	fi

	# Restore the current directory.
	popd >/dev/null 2>&1 || exit
}

verbose_echo() {
	echo_text=${1:-}

	if [ "${VERBOSE_MODE}" -ne 0 ]; then
		echo "${echo_text}"
	fi
}

# Start the main part of the script off with a title.
start_process() {
	verbose_echo "${SCRIPT_TITLE}..."
	verbose_echo ""
	verbose_echo "{Saving current directory prior to execution.}"
	if ! pushd "${SCRIPT_DIR}" >"${TEMP_FILE}" 2>&1; then
		cat "${TEMP_FILE}"
		complete_process 1 "Script cannot save the current directory before proceeding."
	fi

	trap cleanup_function EXIT
}

# Simple function to stop the process with information about why it stopped.
complete_process() {
	local SCRIPT_RETURN_CODE=${1}
	local COMPLETE_REASON=${2:-}

	if [ -n "${COMPLETE_REASON}" ]; then
		echo "${COMPLETE_REASON}"
	fi

	if [ "${SCRIPT_RETURN_CODE}" -ne 0 ]; then
		echo ""
		echo "${SCRIPT_TITLE} failed."
	else
		verbose_echo ""
		verbose_echo "${SCRIPT_TITLE} succeeded."
	fi

	exit "${SCRIPT_RETURN_CODE}"
}

# Give the user hints on how the script can be used.
show_usage() {
	local SCRIPT_NAME=$0

	echo "Usage:"
	echo "  $(basename "${SCRIPT_NAME}") [flags]"
	echo ""
	echo "Summary:"
	echo "  Check for updates to project dependencies managed via pipenv and pre-commit."
	echo ""
	echo "Flags:"
	echo "  -u,--upgrade            Upgrade the dependencies to the latest versions. (default is check only)"
	echo "  -x,--debug              Display debug information about the script as it executes."
	echo "  -q,--quiet              Do not display detailed information during execution."
	echo "  -h,--help               Display this help text."
	echo ""
	exit 1
}

# Parse the command line.
parse_command_line() {

	VERBOSE_MODE=1
	DEBUG_MODE=0
	CHECK_MODE=1
	PARAMS=()
	while (("$#")); do
		case "$1" in

		-u | --upgrade)
			CHECK_MODE=0
			shift
			;;
		-q | --quiet)
			VERBOSE_MODE=0
			shift
			;;
		-x | --debug)
			DEBUG_MODE=1
			shift
			;;
		-h | --help)
			show_usage
			;;
		-*) # unsupported flags
			echo "Error: Unsupported flag ${1}" >&2
			show_usage
			;;
		*) # preserve positional arguments
			PARAMS+=("${1}")
			shift
			;;
		esac
	done

	if [[ ${DEBUG_MODE} -ne 0 ]]; then
		set -x
	fi
}

# Parse any command line values.
parse_command_line "$@"

# Clean entrance into the script.
start_process

# Both tools have issues with UTF-8 on Windows unless these are applied.
export PYTHONIOENCODING=utf-8
# set PYTHONIOENCODING=utf-8

check_for_updates() {
	local PACKAGE_TYPE=${1}
	local DEV_FLAG=${2:-}

	verbose_echo "  Checking ${PACKAGE_TYPE} packages section of Pipfile..."
	verbose_echo "    Exporting ${PACKAGE_TYPE} packages section into requirements file."
	# shellcheck disable=SC2086  # Double quote to prevent splitting and globbing.
	if ! pipenv run python utils/generate_requirements_file.py ${DEV_FLAG} >"${TEMP_FILE2}"; then
		complete_process 1 "Error occurred generating ${PACKAGE_TYPE} requirements file."
	fi

	verbose_echo "    Checking ${PACKAGE_TYPE} packages requirements file."
	if ! pipenv run pcu "${TEMP_FILE2}" >"${TEMP_FILE}" 2>&1; then
		cat "${TEMP_FILE}"
		complete_process 1 "Error occurred checking Pipfile packages updates."
	fi

	# shellcheck disable=SC2086  # Double quote to prevent splitting and globbing.
	if ! PIPFILE_PACKAGES_NEEDING_UPDATING=$(pipenv run python utils/count_remaining_pcu_packages.py ${DEV_FLAG} "${TEMP_FILE}"); then
		complete_process 1 "Error occurred checking filtered Pipfile packages."
	fi
	if [[ "${PIPFILE_PACKAGES_NEEDING_UPDATING}" != "0" ]]; then
		echo "      ${PIPFILE_PACKAGES_NEEDING_UPDATING} Pipfile packages are eligible for updating."
		# shellcheck disable=SC2086  # Double quote to prevent splitting and globbing.
		pipenv run python utils/count_remaining_pcu_packages.py ${DEV_FLAG} "${TEMP_FILE}" --list
		NEED_UPDATE=1
	fi
}

perform_updates() {
	local PACKAGE_TYPE=${1}
	local DEV_FLAG=${2:-}
	local IMPORT_FLAGS=${3:-}

	verbose_echo "  Updating ${PACKAGE_TYPE} packages section of Pipfile..."
	verbose_echo "    Exporting ${PACKAGE_TYPE} packages section into requirements file."
	# shellcheck disable=SC2086  # Double quote to prevent splitting and globbing.
	if ! pipenv run python utils/generate_requirements_file.py ${DEV_FLAG} >"${TEMP_FILE2}"; then
		complete_process 1 "Error occurred generating ${PACKAGE_TYPE} requirements file."
	fi

	verbose_echo "    Upgrading ${PACKAGE_TYPE} packages requirements file."
	if ! pipenv run pcu --upgrade "${TEMP_FILE2}" >"${TEMP_FILE}" 2>&1; then
		cat "${TEMP_FILE}"
		complete_process 1 "Error occurred updating Pipfile packages."
	fi

	verbose_echo "    Importing upgraded requirements file back into ${PACKAGE_TYPE} packages section."
	# shellcheck disable=SC2086  # Double quote to prevent splitting and globbing.
	if ! pipenv install -r "${TEMP_FILE2}" ${IMPORT_FLAGS} >"${TEMP_FILE}" 2>&1; then
		cat "${TEMP_FILE}"
		complete_process 1 "Error occurred installing updated ${PACKAGE_TYPE} packages into pipenv."
	fi
}

if [[ ${CHECK_MODE} -eq 1 ]]; then

	verbose_echo "Checking for Pre-Commit package updates..."
	NEED_UPDATE=0
	if ! pipenv run pre-commit-update --dry-run >"${TEMP_FILE}" 2>&1; then
		echo "One or more Pre-Commit packages are eligible for updating."
		NEED_UPDATE=1
	fi

	verbose_echo "Checking for Pipfile package updates..."

	check_for_updates "standard" ""
	check_for_updates "development" "--dev"

	verbose_echo ""
	if [[ ${NEED_UPDATE} -eq 0 ]]; then
		verbose_echo "All project dependencies are up to date."
	else
		complete_process 2 "One or more project dependencies can be updated."
	fi
else
	verbose_echo "Performing any required Pre-Commit package updates..."
	if ! pipenv run pre-commit-update >"${TEMP_FILE}" 2>&1; then
		cat "${TEMP_FILE}"
		complete_process 1 "Error occurred updating Pre-Commit packages."
	fi

	verbose_echo "Performing any required Pipfile package updates..."

	perform_updates "standard" "" ""
	perform_updates "development" "--dev" "--categories=dev-packages"
fi

# Normal exit from the script.
complete_process 0
