@echo off
setlocal EnableDelayedExpansion
pushd %~dp0

rem Set needed environment variables.
set CLEAN_TEMPFILE=temp_clean.txt
set PYTHON_MODULE_NAME=application_properties

rem Look for options on the command line.

set MY_VERBOSE=
set MY_PUBLISH=
:process_arguments
if "%1" == "-h" (
    echo Command: %0 [options]
    echo   Usage:
    echo     - Execute a clean build for this project.
    echo   Options:
    echo     -h                This message.
	echo     -v                Display verbose information.
	echo     -p				   Publish project summaries if successful.
    GOTO real_end
) else if "%1" == "-v" (
	set MY_VERBOSE=--verbose
) else if "%1" == "-p" (
	set MY_PUBLISH=1
) else if "%1" == "" (
    goto after_process_arguments
) else (
    echo Argument '%1' not understood.  Stopping.
	echo Type '%0 -h' to see valid arguments.
    goto error_end
)
shift
goto process_arguments
:after_process_arguments

rem Announce what this script does.

echo {Analysis of project started.}

rem Cleanly start the main part of the script

echo {Syncing python packages with PipEnv 'pipfile'.}
pipenv sync
if ERRORLEVEL 1 (
	echo.
	echo {Syncing python packages with PipEnv failed.}
	goto error_end
)

echo {Executing black formatter on Python code.}
pipenv run black %MY_VERBOSE% .
if ERRORLEVEL 1 (
	echo.
	echo {Executing black formatter on Python code failed.}
	goto error_end
)

echo {Executing import sorter on Python code.}
pipenv run isort %MY_VERBOSE% .
if ERRORLEVEL 1 (
	echo.
	echo {Executing import sorter on Python code failed.}
	goto error_end
)

echo {Executing pre-commit hooks on Python code.}
pipenv run pre-commit run --all
if ERRORLEVEL 1 (
	echo.
	echo {Executing pre-commit hooks on Python code failed.}
	goto error_end
)

if "%SOURCERY_USER_KEY%" == "" (
	echo {Sourcery user key not defined.  Skipping Sourcery static analyzer.}
) else (
	echo {Executing Sourcery static analyzer on Python code.}
	pipenv run sourcery login --token %SOURCERY_USER_KEY%
	if ERRORLEVEL 1 (
		echo.
		echo {Logging into Sourcery failed.}
		goto error_end
	)
	
	if defined MY_PUBLISH (
		echo {  Executing Sourcery against full project contents.}
		set SOURCERY_LIMIT=
	) else (
		echo {  Executing Sourcery against changed project contents.}
		set "SOURCERY_LIMIT=--diff ^"git diff^""
	)

	pipenv run sourcery review --check %PYTHON_MODULE_NAME% !SOURCERY_LIMIT!
	if ERRORLEVEL 1 (
		echo.
		echo {Executing Sourcery on Python code failed.}
		goto error_end
	)
)

echo {Executing flake8 static analyzer on Python code.}
pipenv run flake8 -j 4 --exclude dist,build %MY_VERBOSE%
if ERRORLEVEL 1 (
	echo.
	echo {Executing static analyzer on Python code failed.}
	goto error_end
)

echo {Executing bandit security analyzer on Python code.}
pipenv run bandit -q -r application_properties
if ERRORLEVEL 1 (
	echo.
	echo {Executing security analyzer on Python code failed.}
	goto error_end
)


echo {Executing pylint static analyzer on source Python code.}
pipenv run pylint -j 4 --rcfile=setup.cfg %MY_VERBOSE% %PYTHON_MODULE_NAME%
if ERRORLEVEL 1 (
	echo.
	echo {Executing pylint static analyzer on source Python code failed.}
	goto error_end
)

echo {Executing mypy static analyzer on Python source code.}
pipenv run mypy --strict %PYTHON_MODULE_NAME%
if ERRORLEVEL 1 (
	echo.
	echo {Executing mypy static analyzer on Python source code failed.}
	goto error_end
)

echo {Executing pylint static analyzer on test Python code.}
pipenv run pylint -j 4 --rcfile=setup.cfg test --ignore test\resources %MY_VERBOSE%
if ERRORLEVEL 1 (
	echo.
	echo {Executing pylint static analyzer on test Python code failed.}
	goto error_end
)

@rem echo {Executing PyMarkdown scan on Markdown documents.}
@rem pipenv run python main.py scan . ./docs
@REM if ERRORLEVEL 1 (
@REM 	echo.
@REM 	echo {PyMarkdown scan on Markdown documents failed.}
@REM 	goto error_end
@REM )

echo {Executing unit tests on Python code.}
call ptest.cmd -c -m
if ERRORLEVEL 1 (
	echo.
	echo {Executing unit tests on Python code failed.}
	goto error_end
)

if defined MY_PUBLISH (
	echo {Publishing summaries after successful analysis of project.}
	call ptest.cmd -p
	if ERRORLEVEL 1 (
		echo.
		echo {Publishing summaries failed.}
		goto error_end
	)
)

rem Cleanly exit the script

echo.
set PC_EXIT_CODE=0
echo {Analysis of project succeeded.}
goto real_end

:error_end
set PC_EXIT_CODE=1
echo {Analysis of project failed.}

:real_end
erase /f /q %CLEAN_TEMPFILE% > nul 2>&1
set CLEAN_TEMPFILE=
popd
exit /B %PC_EXIT_CODE%