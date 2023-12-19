# Things to consider

- I added vscode extension recommendations in the `extensions.json` file. When you open the project in vscode, it should prompt you to install them. I recommend you do so, as they will help with formatting and linting. Also the settings in `.vscode/settings.json` will set the python interpreter to the virtual environment, so your dependencies actually resolve.
- Switch from CRA to Vite (low priority as you already have a working setup)
- Switch from Flask to FastAPI (low)
- Remove reportWebVitals (code in index, file, and also uninstall dependency) and instead use LightHouse (if really necessary)
- Why two charting libs? Seems unnecessary, better stick with one
- I think the python code needs some refactoring regarding the flow and format of the data. Come up with a universal data format for your app and then pass this around instead of working with raw files. What's good is that you already tried to separate business logic (in their own modules) from the HTTP controllers. In the end, the controllers act only as an interface between the client and business logic. They are responsible for request and response validation (body, query, path, parameters, response status code), and error handling. All other logic should be in the business logic modules. I recommend removing all file-related stuff into its own module and interface for the data.
