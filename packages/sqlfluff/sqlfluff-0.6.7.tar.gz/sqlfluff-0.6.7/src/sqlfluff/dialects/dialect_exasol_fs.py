"""The EXASOL dialect for script and function create statements.

This is seperated from the common EXASOL dialect because
`CREATE FUNCTION` and `CREATE SCRIPT` statements are not terminated
by a semicolon. They terminated by a trailing / at the end of the function / script.
A semicolon is the terminator of the statement within the function / script
https://docs.exasol.com
"""

# TODO: How to prevent bracket check in script body?
#       e.g. LUA: local _stmt = [[SOME ASSIGNMENT WITH OPEN BRACKET ( ]]
#                 ...do some stuff ...
#                 local _stmt = _stmt .. [[ ) ]]
# https://github.com/sqlfluff/sqlfluff/issues/1479

from sqlfluff.core.parser import (
    AnyNumberOf,
    Anything,
    BaseSegment,
    Bracketed,
    Delimited,
    BaseFileSegment,
    GreedyUntil,
    OneOf,
    Ref,
    Sequence,
    StartsWith,
    SymbolSegment,
    StringLexer,
    RegexLexer,
    CodeSegment,
    NewlineSegment,
    StringParser,
    NamedParser,
    RegexParser,
)
from sqlfluff.core.dialects import load_raw_dialect

exasol_dialect = load_raw_dialect("exasol")
exasol_fs_dialect = exasol_dialect.copy_as("exasol_fs")
exasol_fs_dialect.sets("unreserved_keywords").add("ROWCOUNT")

exasol_fs_dialect.insert_lexer_matchers(
    [
        StringLexer(
            "walrus_operator",
            ":=",
            CodeSegment,
            segment_kwargs={"type": "walrus_operator"},
        ),
        RegexLexer(
            "function_script_terminator",
            r";\s+\/(?!\*)|\s+\/$",
            CodeSegment,
            segment_kwargs={"type": "statement_terminator"},
            subdivider=StringLexer(
                "semicolon", ";", CodeSegment, segment_kwargs={"type": "semicolon"}
            ),
            trim_post_subdivide=RegexLexer(
                "newline",
                r"(\n|\r\n)+",
                NewlineSegment,
            ),
        ),
        RegexLexer("atsign_literal", r"@[a-zA-Z_][\w]*", CodeSegment),
        RegexLexer("dollar_literal", r"[$][a-zA-Z0-9_.]*", CodeSegment),
    ],
    before="not_equal",
)

exasol_fs_dialect.add(
    FunctionScriptTerminatorSegment=NamedParser(
        "function_script_terminator", CodeSegment, type="statement_terminator"
    ),
    WalrusOperatorSegment=NamedParser(
        "walrus_operator", SymbolSegment, type="assignment_operator"
    ),
    VariableNameSegment=RegexParser(
        r"[A-Z][A-Z0-9_]*",
        CodeSegment,
        name="function_variable",
        type="variable",
    ),
)

exasol_fs_dialect.replace(
    SemicolonSegment=StringParser(
        ";", SymbolSegment, name="semicolon", type="semicolon"
    ),
)


@exasol_fs_dialect.segment(replace=True)
class StatementSegment(BaseSegment):
    """A generic segment, to any of its child subsegments."""

    type = "statement"

    match_grammar = GreedyUntil(Ref("FunctionScriptTerminatorSegment"))
    parse_grammar = OneOf(
        Ref("CreateFunctionStatementSegment"),
        Ref("CreateScriptingLuaScriptStatementSegment"),
        Ref("CreateUDFScriptStatementSegment"),
        Ref("CreateAdapterScriptStatementSegment"),
    )


@exasol_fs_dialect.segment(replace=True)
class FileSegment(BaseFileSegment):
    """This ovewrites the FileSegment from ANSI.

    The reason is because SCRIPT and FUNCTION statements
    are terminated by a trailing / at the end.
    A semicolon is the terminator of the statement within the function / script
    """

    parse_grammar = Delimited(
        Ref("StatementSegment"),
        delimiter=Ref("FunctionScriptTerminatorSegment"),
        allow_gaps=True,
        allow_trailing=True,
    )


############################
# FUNCTION
############################


@exasol_fs_dialect.segment()
class FunctionReferenceSegment(exasol_dialect.get_segment("ObjectReferenceSegment")):  # type: ignore
    """A reference to a function."""

    type = "function_reference"


@exasol_fs_dialect.segment(replace=True)
class CreateFunctionStatementSegment(BaseSegment):
    """A `CREATE FUNCTION` statement."""

    type = "create_function_statement"

    is_ddl = True
    is_dml = False
    is_dql = False
    is_dcl = False

    match_grammar = StartsWith(
        Sequence(
            "CREATE",
            Ref("OrReplaceGrammar", optional=True),
            "FUNCTION",
        )
    )
    parse_grammar = Sequence(
        "CREATE",
        Ref("OrReplaceGrammar", optional=True),
        "FUNCTION",
        Ref("FunctionReferenceSegment"),
        Bracketed(
            Delimited(
                Sequence(
                    Ref("SingleIdentifierGrammar"),  # Column name
                    Ref.keyword("IN", optional=True),
                    Ref("DatatypeSegment"),  # Column type
                ),
                optional=True,
            ),
        ),
        "RETURN",
        Ref("DatatypeSegment"),
        OneOf("IS", "AS", optional=True),
        AnyNumberOf(
            Sequence(
                Ref("VariableNameSegment"),
                Ref("DatatypeSegment"),
                Ref("DelimiterSegment"),
            ),
            optional=True,
        ),
        "BEGIN",
        AnyNumberOf(Ref("FunctionBodySegment")),
        "RETURN",
        Ref("FunctionContentsExpressionGrammar"),
        Ref("DelimiterSegment"),
        "END",
        Ref("FunctionReferenceSegment", optional=True),
        Ref("DelimiterSegment", optional=True),
    )


@exasol_fs_dialect.segment()
class FunctionBodySegment(BaseSegment):
    """The definition of the function body."""

    type = "function_body"
    match_grammar = OneOf(
        Ref("FunctionAssignmentSegment"),
        Ref("FunctionIfBranchSegment"),
        Ref("FunctionForLoopSegment"),
        Ref("FunctionWhileLoopSegment"),
    )


@exasol_fs_dialect.segment()
class FunctionAssignmentSegment(BaseSegment):
    """The definition of a assignment within a function body."""

    type = "function_assignment"
    match_grammar = Sequence(
        # assignment
        Ref("VariableNameSegment"),
        Ref("WalrusOperatorSegment"),
        OneOf(
            Ref("FunctionSegment"),
            Ref("VariableNameSegment"),
            Ref("LiteralGrammar"),
            Ref("ExpressionSegment"),
        ),
        Ref("DelimiterSegment"),
    )


@exasol_fs_dialect.segment()
class FunctionIfBranchSegment(BaseSegment):
    """The definition of a if branch within a function body."""

    type = "function_if_branch"
    match_grammar = Sequence(
        "IF",
        AnyNumberOf(Ref("ExpressionSegment")),
        "THEN",
        AnyNumberOf(Ref("FunctionBodySegment"), min_times=1),
        AnyNumberOf(
            Sequence(
                OneOf("ELSIF", "ELSEIF"),
                Ref("ExpressionSegment"),
                "THEN",
                AnyNumberOf(Ref("FunctionBodySegment"), min_times=1),
            ),
            optional=True,
        ),
        Sequence(
            "ELSE", AnyNumberOf(Ref("FunctionBodySegment"), min_times=1), optional=True
        ),
        "END",
        "IF",
        Ref("DelimiterSegment"),
    )


@exasol_fs_dialect.segment()
class FunctionForLoopSegment(BaseSegment):
    """The definition of a for loop within a function body."""

    type = "function_for_loop"
    match_grammar = Sequence(
        "FOR",
        Ref("NakedIdentifierSegment"),
        OneOf(
            #     # for x := 1 to 10 do...
            Sequence(
                Ref("WalrusOperatorSegment"),
                # Anything(),
                Ref("ExpressionSegment"),  # could be a variable
                "TO",
                Ref("ExpressionSegment"),  # could be a variable
                "DO",
                AnyNumberOf(Ref("FunctionBodySegment"), min_times=1),
                "END",
                "FOR",
            ),
            # for x IN 1..10...
            Sequence(
                "IN",
                Ref("ExpressionSegment"),  # could be a variable
                Ref("RangeOperator"),
                Ref("ExpressionSegment"),  # could be a variable
                "LOOP",
                AnyNumberOf(Ref("FunctionBodySegment"), min_times=1),
                "END",
                "LOOP",
            ),
        ),
        Ref("DelimiterSegment"),
    )


@exasol_fs_dialect.segment()
class FunctionWhileLoopSegment(BaseSegment):
    """The definition of a while loop within a function body."""

    type = "function_while_loop"
    match_grammar = Sequence(
        "WHILE",
        Ref("ExpressionSegment"),
        "DO",
        AnyNumberOf(Ref("FunctionBodySegment"), min_times=1),
        "END",
        "WHILE",
        Ref("DelimiterSegment"),
    )


############################
# SCRIPT
############################
@exasol_fs_dialect.segment()
class ScriptReferenceSegment(exasol_dialect.get_segment("ObjectReferenceSegment")):  # type: ignore
    """A reference to a script."""

    type = "script_reference"


@exasol_fs_dialect.segment()
class ScriptContentSegment(BaseSegment):
    """This represents the script content.

    Because the script content could be written in
    LUA, PYTHON, JAVA or R there is no further verification.
    """

    type = "script_content"
    match_grammar = Anything()


@exasol_fs_dialect.segment()
class CreateScriptingLuaScriptStatementSegment(BaseSegment):
    """`CREATE SCRIPT` statement to create a Lua scripting script.

    https://docs.exasol.com/sql/create_script.htm
    """

    type = "create_scripting_lua_script"

    is_ddl = True
    is_dml = False
    is_dql = False
    is_dcl = False

    match_grammar = StartsWith(
        Sequence(
            "CREATE",
            Ref("OrReplaceGrammar", optional=True),
            Ref.keyword("LUA", optional=True),
            "SCRIPT",
        )
    )
    parse_grammar = Sequence(
        "CREATE",
        Ref("OrReplaceGrammar", optional=True),
        Ref.keyword("LUA", optional=True),
        "SCRIPT",
        Ref("ScriptReferenceSegment"),
        Bracketed(
            Delimited(
                Sequence(
                    Ref.keyword("ARRAY", optional=True), Ref("SingleIdentifierGrammar")
                ),
                optional=True,
            ),
            optional=True,
        ),
        Sequence(Ref.keyword("RETURNS"), OneOf("TABLE", "ROWCOUNT"), optional=True),
        "AS",
        Ref("ScriptContentSegment"),
    )


@exasol_fs_dialect.segment()
class CreateUDFScriptStatementSegment(BaseSegment):
    """`CREATE SCRIPT` statement create a UDF script.

    https://docs.exasol.com/sql/create_script.htm
    """

    type = "create_udf_script"

    is_ddl = True
    is_dml = False
    is_dql = False
    is_dcl = False

    match_grammar = StartsWith(
        Sequence(
            "CREATE",
            Ref("OrReplaceGrammar", optional=True),
            OneOf(
                "JAVA",
                "PYTHON",
                "LUA",
                "R",
                Ref("SingleIdentifierGrammar"),
                optional=True,
            ),
            OneOf("SCALAR", "SET"),
            "SCRIPT",
        )
    )
    parse_grammar = Sequence(
        "CREATE",
        Ref("OrReplaceGrammar", optional=True),
        OneOf(
            "JAVA", "PYTHON", "LUA", "R", Ref("SingleIdentifierGrammar"), optional=True
        ),
        OneOf("SCALAR", "SET"),
        "SCRIPT",
        Ref("ScriptReferenceSegment"),
        Bracketed(
            Sequence(
                Delimited(Ref("ColumnDatatypeSegment")),
                Ref("OrderByClauseSegment", optional=True),
                optional=True,
            ),
            optional=True,
        ),
        OneOf(Sequence("RETURNS", Ref("DatatypeSegment")), Ref("EmitsGrammar")),
        "AS",
        Ref("ScriptContentSegment"),
    )


@exasol_fs_dialect.segment()
class CreateAdapterScriptStatementSegment(BaseSegment):
    """`CREATE SCRIPT` statement create a adapter script.

    https://docs.exasol.com/sql/create_script.htm
    """

    type = "create_adapter_script"

    is_ddl = True
    is_dml = False
    is_dql = False
    is_dcl = False

    match_grammar = StartsWith(
        "CREATE",
        Ref("OrReplaceGrammar", optional=True),
        OneOf("JAVA", "PYTHON", Ref("SingleIdentifierGrammar"), optional=True),
        "ADAPTER",
        "SCRIPT",
    )
    parse_grammar = Sequence(
        "CREATE",
        Ref("OrReplaceGrammar", optional=True),
        OneOf("JAVA", "PYTHON", Ref("SingleIdentifierGrammar"), optional=True),
        "ADAPTER",
        "SCRIPT",
        Ref("ScriptReferenceSegment"),
        Ref("ScriptContentSegment"),
    )
