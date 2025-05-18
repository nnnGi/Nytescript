import os
import json

# Install CLI
try:
    os.system('cd .')
    os.system('pip install poetry')
    os.system('poetry self add poetry-plugin-shell')
    os.system('poetry install')
    os.system('pip install --editable .')
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Completed CLI installation')
except Exception as e:
    print(f'Failed with Exception {e}')

try:
    # Determine the correct path to settings.json based on the operating system
    if os.name == 'nt': # Windows
        settings_path = os.path.join(os.environ.get('APPDATA'), 'Code', 'User', 'settings.json')
    else: # macOS or Linux
        settings_path = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'Code', 'User', 'settings.json')

    print(f"Attempting to modify settings file at: {settings_path}")

    if not os.path.exists(settings_path):
        print(f'Visual Studio Code Settings.json not found at {settings_path}. Cannot modify.')
        exit()

    base_settings_content = """
{
    "security.workspace.trust.untrustedFiles": "open",
    "workbench.editorAssociations": {
        "*.zip": "default"
    },
    "python.defaultInterpreterPath": "",
    "files.autoSave": "afterDelay",
    "window.zoomLevel": 1,
    "python.createEnvironment.trigger": "off",
    "terminal.integrated.fontFamily": "'NotoMono Nerd Font'",
    "editor.semanticHighlighting.enabled": true,
    "emmet.syntaxProfiles": {

    },
    "workbench.colorTheme": "One Dark Pro Darker",
    "[python]": {

        "diffEditor.ignoreTrimWhitespace": false,
        "editor.defaultColorDecorators": "never",
        "editor.formatOnType": true,
        "editor.wordBasedSuggestions": "off"
    },
    "python.analysis.autoFormatStrings": true,
    "editor.cursorSmoothCaretAnimation": "on",
    "[json]": {
        "editor.defaultFormatter": "vscode.json-language-features"
    },
    "code-runner.executorMapByFileExtension": {

        ".vb": "cd $dir && vbc /nologo $fileName && $dir$fileNameWithoutExt",
        ".vbs": "cscript //Nologo",
        ".scala": "scala",
        ".jl": "julia",
        ".cr": "crystal",
        ".ml": "ocaml",
        ".zig": "zig run",
        ".exs": "elixir",
        ".hx": "haxe --cwd $dirWithoutTrailingSlash --run $fileNameWithoutExt",
        ".rkt": "racket",
        ".scm": "csi -script",
        ".ahk": "autohotkey",
        ".au3": "autoit3",
        ".kt": "cd $dir && kotlinc $fileName -include-runtime -d $fileNameWithoutExt.jar && java -jar $fileNameWithoutExt.jar",
        ".kts": "kotlinc -script",
        ".dart": "dart",
        ".pas": "cd $dir && fpc $fileName && $dir$fileNameWithoutExt",
        ".pp": "cd $dir && fpc $fileName && $dir$fileNameWithoutExt",
        ".d": "cd $dir && dmd $fileName && $dir$fileNameWithoutExt",
        ".hs": "runhaskell",
        ".nim": "nim compile --verbosity:0 --hints:off --run",
        ".csproj": "dotnet run --project",
        ".fsproj": "dotnet run --project",
        ".lisp": "sbcl --script",
        ".kit": "kitc --run",
        ".v": "v run",
        ".vsh": "v run",
        ".sass": "sass --style expanded",
        ".cu": "cd $dir && nvcc $fileName -o $fileNameWithoutExt && $dir$fileNameWithoutExt",
        ".ring": "ring",
        ".sml": "cd $dir && sml $fileName",
        ".mojo": "mojo run",
        ".erl": "escript",
        ".spwn": "spwn build",
        ".pkl": "cd $dir && pkl eval -f yaml $fileName -o $fileNameWithoutExt.yaml",
        ".gleam": "gleam run -m $fileNameWithoutExt",
        ".ns": "nytescript $fileNameWithoutExt.ns"
    },
    "code-runner.runInTerminal": true,
    "code-runner.saveAllFilesBeforeRun": true,
    "code-runner.saveFileBeforeRun": true,
    "code-runner.executorMap": {
        "javascript": "node",
        "java": "cd $dir && javac $fileName && java $fileNameWithoutExt",
        "c": "cd $dir && gcc $fileName -o $fileNameWithoutExt && $dir$fileNameWithoutExt",
        "zig": "zig run",
        "cpp": "cd $dir && g++ $fileName -o $fileNameWithoutExt && $dir$fileNameWithoutExt",
        "objective-c": "cd $dir && gcc -framework Cocoa $fileName -o $fileNameWithoutExt && $dir$fileNameWithoutExt",
        "php": "php",
        "python": "python -u",
        "perl": "perl",
        "perl6": "perl6",
        "ruby": "ruby",
        "go": "go run",
        "lua": "lua",
        "groovy": "groovy",
        "powershell": "powershell -ExecutionPolicy ByPass -File",
        "bat": "cmd /c",
        "shellscript": "bash",
        "fsharp": "fsi",
        "csharp": "scriptcs",
        "vbscript": "cscript //Nologo",
        "typescript": "ts-node",
        "coffeescript": "coffee",
        "scala": "scala",
        "swift": "swift",
        "julia": "julia",
        "crystal": "crystal",
        "ocaml": "ocaml",
        "r": "Rscript",
        "applescript": "osascript",
        "clojure": "lein exec",
        "haxe": "haxe --cwd $dirWithoutTrailingSlash --run $fileNameWithoutExt",
        "rust": "cd $dir && rustc $fileName && $dir$fileNameWithoutExt",
        "racket": "racket",
        "scheme": "csi -script",
        "ahk": "autohotkey",
        "autoit": "autoit3",
        "dart": "dart",
        "pascal": "cd $dir && fpc $fileName && $dir$fileNameWithoutExt",
        "d": "cd $dir && dmd $fileName && $dir$fileNameWithoutExt",
        "haskell": "runghc",
        "nim": "nim compile --verbosity:0 --hints:off --run",
        "lisp": "sbcl --script",
        "kit": "kitc --run",
        "v": "v run",
        "sass": "sass --style expanded",
        "scss": "scss --style expanded",
        "less": "cd $dir && lessc $fileName $fileNameWithoutExt.css",
        "FortranFreeForm": "cd $dir && gfortran $fileName -o $fileNameWithoutExt && $dir$fileNameWithoutExt",
        "fortran-modern": "cd $dir && gfortran $fileName -o $fileNameWithoutExt && $dir$fileNameWithoutExt",
        "fortran_fixed-form": "cd $dir && gfortran $fileName -o $fileNameWithoutExt && $dir$fileNameWithoutExt",
        "fortran": "cd $dir && gfortran $fileName -o $fileNameWithoutExt && $dir$fileNameWithoutExt",
        "sml": "cd $dir && sml $fileName",
        "mojo": "mojo run",
        "erlang": "escript",
        "spwn": "spwn build",
        "pkl": "cd $dir && pkl eval -f yaml $fileName -o $fileNameWithoutExt.yaml",
        "gleam": "gleam run -m $fileNameWithoutExt",
        "nytescript": "nytescript $fileNameWithoutExt.ns"
    },
    "code-runner.languageIdToFileExtensionMap": {
        "nytescript": ".ns",
        "bat": ".bat",
        "powershell": ".ps1",
        "typescript": ".ts"
    },
    "code-runner.executorMapByGlob": {
        "pom.xml": "cd $dir && mvn clean package"
    }
}
"""
    # --- END OF BASE SETTINGS CONTENT ---

    # --- Keys to preserve from the existing file ---
    # Add any other settings keys you want to preserve here
    settings_to_preserve = [
        "editor.fontFamily",
        "editor.fontSize", # Font size is often related to font settings
        "workbench.colorTheme",
        "workbench.iconTheme", # Icon theme
        "terminal.integrated.fontFamily", # Terminal font
        "terminal.integrated.fontSize" # Terminal font size
        # Add more keys here if needed, e.g., "editor.tabSize"
    ]

    # Read the existing settings file
    with open(settings_path, 'r') as file:
        existing_content = file.read()

    # Parse the existing and base content as JSON
    try:
        existing_data = json.loads(existing_content)
        base_data = json.loads(base_settings_content)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON. Please check the syntax of your existing settings.json or the base_settings_content: {e}")
        exit() # Exit if JSON is invalid

    # Extract settings to preserve from the existing data
    preserved_settings = {}
    for key in settings_to_preserve:
        if key in existing_data:
            preserved_settings[key] = existing_data[key]

    # Merge the preserved settings into the base data
    # This updates base_data with values from preserved_settings,
    # effectively overriding the base settings if the keys exist in preserved_settings.
    base_data.update(preserved_settings)

    # Convert the merged data back to a formatted JSON string
    # use indent=4 for readability
    merged_content = json.dumps(base_data, indent=4)

    # Write the merged content back to the settings file
    with open(settings_path, 'w') as file:
        file.write(merged_content)

    print(f"Successfully updated {settings_path}, preserving specified settings.")

except FileNotFoundError:
    print(f'Visual Studio Code Settings.json not found at {settings_path}. Cannot modify.')
except KeyError:
    print("APPDATA environment variable not found. This might not be a standard Windows environment or the script is run in an unusual context.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")