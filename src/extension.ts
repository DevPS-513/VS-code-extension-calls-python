// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';
// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "pytest-bdd-go-to-step" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	const disposable = vscode.commands.registerCommand('pytest-bdd-go-to-step.helloWorld', () => {
		// The code you place here will be executed every time your command is executed
		// Display a message box to the user
		vscode.window.showInformationMessage('Hello World from Pytest-BDD-go-to-step!');
	});

	    // Register the "navigateToCode" command
		const navigateToCodeDisposable = vscode.commands.registerCommand('pytest-bdd-go-to-step.navigateToCode', () => {
			const editor = vscode.window.activeTextEditor;
			vscode.window.showInformationMessage('Hello from navigateToCode');

			const scriptPath = path.join(context.extensionPath, 'pyscript.py');
			exec(`python3 ${scriptPath}`, (error, stdout, stderr) => {
				if (error) {
					vscode.window.showErrorMessage(`Error: ${error.message}`);
					return;
				}
				if (stderr) {
					vscode.window.showErrorMessage(`Stderr: ${stderr}`);
					return;
				}
				vscode.window.showInformationMessage(`Output: ${stdout}`);
			});

			if (editor) {
				const document = editor.document;
				const position = editor.selection.active;
	
				// Example: Navigate to the start of the document
				const newPosition = new vscode.Position(0, 0);
				const newSelection = new vscode.Selection(newPosition, newPosition);
	
				editor.selection = newSelection;
				editor.revealRange(new vscode.Range(newPosition, newPosition));

				

			}
		});


	
	
		context.subscriptions.push(navigateToCodeDisposable);

	context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}
