import { IConnection, InitializeParams, InitializeResult, TextDocument, TextDocumentChangeEvent } from 'vscode-languageserver';
import { AbstractLanguageServer } from 'stardog-language-utils';
import { TurtleParser } from 'millan';
export declare class TurtleLanguageServer extends AbstractLanguageServer<TurtleParser> {
    private mode;
    constructor(connection: IConnection);
    onInitialization(params: InitializeParams): InitializeResult;
    onContentChange({ document }: TextDocumentChangeEvent, parseResults: ReturnType<AbstractLanguageServer<TurtleParser>['parseDocument']>): void;
    parseDocument(document: TextDocument): {
        cst: any;
        tokens: import("chevrotain").IToken[];
        errors: import("chevrotain").IRecognitionException[];
        otherParseData: Pick<{
            errors: import("chevrotain").IRecognitionException[];
            semanticErrors: import("chevrotain").IRecognitionException[];
            cst: any;
        }, "semanticErrors">;
    };
}
