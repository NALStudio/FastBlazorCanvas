from typing import Final as _F
import parse as _parse

ts2cs_translationtable: _F[dict[str, str]] = {
    "void": "void",
    "number": "double",
    "boolean": "bool",
    "string": "string",
    "Uint8ClampedArray": "byte[]",
}

do_not_resolve: _F[frozenset[str]] = frozenset({
    # reference DOM elements that we don't want to resolve
    "HTMLCanvasElement",
    "CanvasUserInterface",
    "DOMMatrix",

    # Canvas extensions
    "CanvasFillStrokeStyles", # Cannot marshal union types, write string functions manually
    "CanvasDrawImage", # Depends on CanvasImageSource which cannot be marshaled (union impossible to generate as a whole)

    # Ignore DOMMatrix instead
    # as CanvasTransform seems to have easily parsable functions
    # "CanvasTransform",

    # has 'maybe' parameters (parameters that either exist or don't which sounds like a pain in the ass to implement)
    "CanvasRenderingContext2DSettings", # we can roll our own very easily for GetContext()... although it can't be retrieved from the context itself
})

forbidden_type_in_parse: _F[frozenset[str]] = frozenset({
    "CanvasImageSource"
})

context_to_resolve: _F[str] ="CanvasRenderingContext2D"
context_remove_members: _F[frozenset[str]] = frozenset({
    "roundRect", # union impossible to generate in C#

    "getTransform", # Refer to DOMMatrix
    "setTransform",

    "canvas", # HTMLCanvasElement not resolved
    "getContextAttributes", # CanvasRenderingContext2DSettings not resolved
})
context_add_custom_members: _F[tuple[_parse.Member, ...]] = (
    _parse.Field("fillStyle",   _parse.SingleType("string"), readonly=False),
    _parse.Field("strokeStyle", _parse.SingleType("string"), readonly=False),

    # TODO: Support overloads so that we can also have a per corner radius
    _parse.Method("roundRect", _parse.SingleType("void"), arguments=(
        _parse.MethodArgument("x", _parse.SingleType("number"), optional=False),
        _parse.MethodArgument("y", _parse.SingleType("number"), optional=False),
        _parse.MethodArgument("w", _parse.SingleType("number"), optional=False),
        _parse.MethodArgument("h", _parse.SingleType("number"), optional=False),
        _parse.MethodArgument("radii", _parse.SingleType("number"), optional=True),
    ))
)

# Does not include context_to_resolve, this is built automatically
cs_generate_classes_for_interfaces: _F[frozenset[str]] = frozenset({
    "ImageData",
    "Path2D",
    "TextMetrics"
})

CS_NAMESPACE: _F[str] = "FastBlazorCanvas.Contexts"
JS_MODULE_NAME: _F[str] = "NDPCanvas_SOURCEGEN"
