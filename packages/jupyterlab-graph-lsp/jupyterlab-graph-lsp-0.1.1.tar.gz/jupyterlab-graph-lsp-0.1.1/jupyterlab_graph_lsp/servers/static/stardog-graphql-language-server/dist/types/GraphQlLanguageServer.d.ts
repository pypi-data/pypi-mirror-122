import { InitializeResult, TextDocumentChangeEvent, InitializeParams, IConnection, TextDocumentPositionParams, CompletionItem, CompletionItemKind, TextDocument, Diagnostic } from 'vscode-languageserver';
import { SparqlCompletionData, AbstractLanguageServer } from 'stardog-language-utils';
import { ISemanticError, StandardGraphQlParser, StardogGraphQlParser } from 'millan';
export declare class GraphQlLanguageServer extends AbstractLanguageServer<StardogGraphQlParser | StandardGraphQlParser> {
    protected parser: StardogGraphQlParser | StandardGraphQlParser;
    private namespaceMap;
    private relationshipBindings;
    private relationshipCompletionItems;
    private typeBindings;
    private typeCompletionItems;
    private graphQLValueTypeBindings;
    private graphQLTypeCompletionItems;
    constructor(connection: IConnection);
    onInitialization(params: InitializeParams): InitializeResult;
    handleUpdateCompletionData(update: SparqlCompletionData): void;
    buildCompletionItemsFromData(namespaceMap: {
        [alias: string]: string;
    }, irisAndCounts: {
        iri: string;
        count: string;
    }[], kind: CompletionItemKind): CompletionItem[];
    buildGraphQLTypeCompletionItems(namespaceMap: {
        [alias: string]: string;
    }, typesAndIris: {
        type: string;
        iri: string;
    }[]): CompletionItem[];
    private addStardogSpecificDirectivesToCompletionCandidates;
    private addArgumentsToCandidatesWithoutDupes;
    private addStardogSpecificArgumentsToCompletionCandidates;
    handleCompletion(params: TextDocumentPositionParams): CompletionItem[];
    private getCompletionItem;
    onContentChange({ document }: TextDocumentChangeEvent, parseResult: ReturnType<AbstractLanguageServer<StardogGraphQlParser | StandardGraphQlParser>['parseDocument']>): void;
    getParseDiagnostics(document: TextDocument, errors: ISemanticError[]): Diagnostic[];
}
