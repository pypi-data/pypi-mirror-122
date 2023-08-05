import { CompletionItem, IConnection, InitializeParams, InitializeResult, TextDocument, TextDocumentChangeEvent, TextDocumentPositionParams, TextEdit } from 'vscode-languageserver';
import { StardogSparqlParser, W3SpecSparqlParser } from 'millan';
import { SparqlCompletionData, AbstractLanguageServer, CompletionCandidate } from 'stardog-language-utils';
import { IToken } from 'chevrotain';
export declare class SparqlLanguageServer extends AbstractLanguageServer<StardogSparqlParser | W3SpecSparqlParser> {
    protected parser: StardogSparqlParser | W3SpecSparqlParser;
    private namespaceMap;
    private relationshipBindings;
    private relationshipCompletionItems;
    private typeBindings;
    private typeCompletionItems;
    constructor(connection: IConnection);
    onInitialization(params: InitializeParams): InitializeResult;
    handleUpdateCompletionData(update: SparqlCompletionData): void;
    buildCompletionItemsFromData(namespaceMap: any, irisAndCounts: {
        iri: string;
        count: string;
    }[]): CompletionItem[];
    replaceTokenAtCursor({ document, replacement, replacementRange, tokenAtCursor, }: {
        document: TextDocument;
        replacement: string;
        replacementRange?: CompletionCandidate['replacementRange'];
        tokenAtCursor: IToken;
    }): TextEdit;
    getRelationshipCompletions(document: TextDocument, tokenAtCursor: IToken): any[];
    getClassCompletions(document: TextDocument, tokenAtCursor: IToken): any[];
    handleCompletion(params: TextDocumentPositionParams): CompletionItem[];
    onContentChange({ document }: TextDocumentChangeEvent, parseResult: ReturnType<AbstractLanguageServer<StardogSparqlParser | W3SpecSparqlParser>['parseDocument']>): void;
}
