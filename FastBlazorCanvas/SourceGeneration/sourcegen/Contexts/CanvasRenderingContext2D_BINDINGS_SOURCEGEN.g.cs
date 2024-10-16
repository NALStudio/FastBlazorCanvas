/* AUTO GENERATED CODE */

using System.Runtime.InteropServices.JavaScript;

namespace FastBlazorCanvas.Contexts;

[System.Runtime.Versioning.SupportedOSPlatform("browser")]
internal partial class CanvasRenderingContext2DBindings
{
    [JSImport("CanvasRenderingContext2D_property_get_globalAlpha", "NDPCanvas_SOURCEGEN")]
    public static partial double GetGlobalAlpha(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_globalAlpha", "NDPCanvas_SOURCEGEN")]
    public static partial void SetGlobalAlpha(JSObject obj, double value);

    [JSImport("CanvasRenderingContext2D_property_get_globalCompositeOperation", "NDPCanvas_SOURCEGEN")]
    public static partial string GetGlobalCompositeOperation(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_globalCompositeOperation", "NDPCanvas_SOURCEGEN")]
    public static partial void SetGlobalCompositeOperation(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_method_beginPath", "NDPCanvas_SOURCEGEN")]
    public static partial void BeginPath(JSObject obj);

    [JSImport("CanvasRenderingContext2D_method_clip", "NDPCanvas_SOURCEGEN")]
    public static partial void Clip(JSObject obj);

    [JSImport("CanvasRenderingContext2D_method_clip_opt", "NDPCanvas_SOURCEGEN")]
    public static partial void Clip(JSObject obj, string fillRule);

    [JSImport("CanvasRenderingContext2D_method_clip", "NDPCanvas_SOURCEGEN")]
    public static partial void Clip(JSObject obj, Path2D path);

    [JSImport("CanvasRenderingContext2D_method_clip_opt", "NDPCanvas_SOURCEGEN")]
    public static partial void Clip(JSObject obj, Path2D path, string fillRule);

    [JSImport("CanvasRenderingContext2D_method_fill", "NDPCanvas_SOURCEGEN")]
    public static partial void Fill(JSObject obj);

    [JSImport("CanvasRenderingContext2D_method_fill_opt", "NDPCanvas_SOURCEGEN")]
    public static partial void Fill(JSObject obj, string fillRule);

    [JSImport("CanvasRenderingContext2D_method_fill", "NDPCanvas_SOURCEGEN")]
    public static partial void Fill(JSObject obj, Path2D path);

    [JSImport("CanvasRenderingContext2D_method_fill_opt", "NDPCanvas_SOURCEGEN")]
    public static partial void Fill(JSObject obj, Path2D path, string fillRule);

    [JSImport("CanvasRenderingContext2D_method_isPointInPath", "NDPCanvas_SOURCEGEN")]
    public static partial bool IsPointInPath(JSObject obj, double x, double y);

    [JSImport("CanvasRenderingContext2D_method_isPointInPath_opt", "NDPCanvas_SOURCEGEN")]
    public static partial bool IsPointInPath(JSObject obj, double x, double y, string fillRule);

    [JSImport("CanvasRenderingContext2D_method_isPointInPath", "NDPCanvas_SOURCEGEN")]
    public static partial bool IsPointInPath(JSObject obj, Path2D path, double x, double y);

    [JSImport("CanvasRenderingContext2D_method_isPointInPath_opt", "NDPCanvas_SOURCEGEN")]
    public static partial bool IsPointInPath(JSObject obj, Path2D path, double x, double y, string fillRule);

    [JSImport("CanvasRenderingContext2D_method_isPointInStroke", "NDPCanvas_SOURCEGEN")]
    public static partial bool IsPointInStroke(JSObject obj, double x, double y);

    [JSImport("CanvasRenderingContext2D_method_isPointInStroke", "NDPCanvas_SOURCEGEN")]
    public static partial bool IsPointInStroke(JSObject obj, Path2D path, double x, double y);

    [JSImport("CanvasRenderingContext2D_method_stroke", "NDPCanvas_SOURCEGEN")]
    public static partial void Stroke(JSObject obj);

    [JSImport("CanvasRenderingContext2D_method_stroke", "NDPCanvas_SOURCEGEN")]
    public static partial void Stroke(JSObject obj, Path2D path);

    [JSImport("CanvasRenderingContext2D_property_get_filter", "NDPCanvas_SOURCEGEN")]
    public static partial string GetFilter(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_filter", "NDPCanvas_SOURCEGEN")]
    public static partial void SetFilter(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_property_get_imageSmoothingEnabled", "NDPCanvas_SOURCEGEN")]
    public static partial bool GetImageSmoothingEnabled(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_imageSmoothingEnabled", "NDPCanvas_SOURCEGEN")]
    public static partial void SetImageSmoothingEnabled(JSObject obj, bool value);

    [JSImport("CanvasRenderingContext2D_property_get_imageSmoothingQuality", "NDPCanvas_SOURCEGEN")]
    public static partial string GetImageSmoothingQuality(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_imageSmoothingQuality", "NDPCanvas_SOURCEGEN")]
    public static partial void SetImageSmoothingQuality(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_method_arc", "NDPCanvas_SOURCEGEN")]
    public static partial void Arc(JSObject obj, double x, double y, double radius, double startAngle, double endAngle);

    [JSImport("CanvasRenderingContext2D_method_arc_opt", "NDPCanvas_SOURCEGEN")]
    public static partial void Arc(JSObject obj, double x, double y, double radius, double startAngle, double endAngle, bool counterclockwise);

    [JSImport("CanvasRenderingContext2D_method_arcTo", "NDPCanvas_SOURCEGEN")]
    public static partial void ArcTo(JSObject obj, double x1, double y1, double x2, double y2, double radius);

    [JSImport("CanvasRenderingContext2D_method_bezierCurveTo", "NDPCanvas_SOURCEGEN")]
    public static partial void BezierCurveTo(JSObject obj, double cp1x, double cp1y, double cp2x, double cp2y, double x, double y);

    [JSImport("CanvasRenderingContext2D_method_closePath", "NDPCanvas_SOURCEGEN")]
    public static partial void ClosePath(JSObject obj);

    [JSImport("CanvasRenderingContext2D_method_ellipse", "NDPCanvas_SOURCEGEN")]
    public static partial void Ellipse(JSObject obj, double x, double y, double radiusX, double radiusY, double rotation, double startAngle, double endAngle);

    [JSImport("CanvasRenderingContext2D_method_ellipse_opt", "NDPCanvas_SOURCEGEN")]
    public static partial void Ellipse(JSObject obj, double x, double y, double radiusX, double radiusY, double rotation, double startAngle, double endAngle, bool counterclockwise);

    [JSImport("CanvasRenderingContext2D_method_lineTo", "NDPCanvas_SOURCEGEN")]
    public static partial void LineTo(JSObject obj, double x, double y);

    [JSImport("CanvasRenderingContext2D_method_moveTo", "NDPCanvas_SOURCEGEN")]
    public static partial void MoveTo(JSObject obj, double x, double y);

    [JSImport("CanvasRenderingContext2D_method_quadraticCurveTo", "NDPCanvas_SOURCEGEN")]
    public static partial void QuadraticCurveTo(JSObject obj, double cpx, double cpy, double x, double y);

    [JSImport("CanvasRenderingContext2D_method_rect", "NDPCanvas_SOURCEGEN")]
    public static partial void Rect(JSObject obj, double x, double y, double w, double h);

    [JSImport("CanvasRenderingContext2D_property_get_lineCap", "NDPCanvas_SOURCEGEN")]
    public static partial string GetLineCap(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_lineCap", "NDPCanvas_SOURCEGEN")]
    public static partial void SetLineCap(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_property_get_lineDashOffset", "NDPCanvas_SOURCEGEN")]
    public static partial double GetLineDashOffset(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_lineDashOffset", "NDPCanvas_SOURCEGEN")]
    public static partial void SetLineDashOffset(JSObject obj, double value);

    [JSImport("CanvasRenderingContext2D_property_get_lineJoin", "NDPCanvas_SOURCEGEN")]
    public static partial string GetLineJoin(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_lineJoin", "NDPCanvas_SOURCEGEN")]
    public static partial void SetLineJoin(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_property_get_lineWidth", "NDPCanvas_SOURCEGEN")]
    public static partial double GetLineWidth(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_lineWidth", "NDPCanvas_SOURCEGEN")]
    public static partial void SetLineWidth(JSObject obj, double value);

    [JSImport("CanvasRenderingContext2D_property_get_miterLimit", "NDPCanvas_SOURCEGEN")]
    public static partial double GetMiterLimit(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_miterLimit", "NDPCanvas_SOURCEGEN")]
    public static partial void SetMiterLimit(JSObject obj, double value);

    [JSImport("CanvasRenderingContext2D_method_getLineDash", "NDPCanvas_SOURCEGEN")]
    public static partial double[] GetLineDash(JSObject obj);

    [JSImport("CanvasRenderingContext2D_method_setLineDash", "NDPCanvas_SOURCEGEN")]
    public static partial void SetLineDash(JSObject obj, double[] segments);

    [JSImport("CanvasRenderingContext2D_method_clearRect", "NDPCanvas_SOURCEGEN")]
    public static partial void ClearRect(JSObject obj, double x, double y, double w, double h);

    [JSImport("CanvasRenderingContext2D_method_fillRect", "NDPCanvas_SOURCEGEN")]
    public static partial void FillRect(JSObject obj, double x, double y, double w, double h);

    [JSImport("CanvasRenderingContext2D_method_strokeRect", "NDPCanvas_SOURCEGEN")]
    public static partial void StrokeRect(JSObject obj, double x, double y, double w, double h);

    [JSImport("CanvasRenderingContext2D_property_get_shadowBlur", "NDPCanvas_SOURCEGEN")]
    public static partial double GetShadowBlur(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_shadowBlur", "NDPCanvas_SOURCEGEN")]
    public static partial void SetShadowBlur(JSObject obj, double value);

    [JSImport("CanvasRenderingContext2D_property_get_shadowColor", "NDPCanvas_SOURCEGEN")]
    public static partial string GetShadowColor(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_shadowColor", "NDPCanvas_SOURCEGEN")]
    public static partial void SetShadowColor(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_property_get_shadowOffsetX", "NDPCanvas_SOURCEGEN")]
    public static partial double GetShadowOffsetX(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_shadowOffsetX", "NDPCanvas_SOURCEGEN")]
    public static partial void SetShadowOffsetX(JSObject obj, double value);

    [JSImport("CanvasRenderingContext2D_property_get_shadowOffsetY", "NDPCanvas_SOURCEGEN")]
    public static partial double GetShadowOffsetY(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_shadowOffsetY", "NDPCanvas_SOURCEGEN")]
    public static partial void SetShadowOffsetY(JSObject obj, double value);

    [JSImport("CanvasRenderingContext2D_method_isContextLost", "NDPCanvas_SOURCEGEN")]
    public static partial bool IsContextLost(JSObject obj);

    [JSImport("CanvasRenderingContext2D_method_reset", "NDPCanvas_SOURCEGEN")]
    public static partial void Reset(JSObject obj);

    [JSImport("CanvasRenderingContext2D_method_restore", "NDPCanvas_SOURCEGEN")]
    public static partial void Restore(JSObject obj);

    [JSImport("CanvasRenderingContext2D_method_save", "NDPCanvas_SOURCEGEN")]
    public static partial void Save(JSObject obj);

    [JSImport("CanvasRenderingContext2D_method_fillText", "NDPCanvas_SOURCEGEN")]
    public static partial void FillText(JSObject obj, string text, double x, double y);

    [JSImport("CanvasRenderingContext2D_method_fillText_opt", "NDPCanvas_SOURCEGEN")]
    public static partial void FillText(JSObject obj, string text, double x, double y, double maxWidth);

    [JSImport("CanvasRenderingContext2D_method_measureText", "NDPCanvas_SOURCEGEN")]
    public static partial TextMetrics MeasureText(JSObject obj, string text);

    [JSImport("CanvasRenderingContext2D_method_strokeText", "NDPCanvas_SOURCEGEN")]
    public static partial void StrokeText(JSObject obj, string text, double x, double y);

    [JSImport("CanvasRenderingContext2D_method_strokeText_opt", "NDPCanvas_SOURCEGEN")]
    public static partial void StrokeText(JSObject obj, string text, double x, double y, double maxWidth);

    [JSImport("CanvasRenderingContext2D_property_get_direction", "NDPCanvas_SOURCEGEN")]
    public static partial string GetDirection(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_direction", "NDPCanvas_SOURCEGEN")]
    public static partial void SetDirection(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_property_get_font", "NDPCanvas_SOURCEGEN")]
    public static partial string GetFont(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_font", "NDPCanvas_SOURCEGEN")]
    public static partial void SetFont(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_property_get_fontKerning", "NDPCanvas_SOURCEGEN")]
    public static partial string GetFontKerning(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_fontKerning", "NDPCanvas_SOURCEGEN")]
    public static partial void SetFontKerning(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_property_get_fontStretch", "NDPCanvas_SOURCEGEN")]
    public static partial string GetFontStretch(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_fontStretch", "NDPCanvas_SOURCEGEN")]
    public static partial void SetFontStretch(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_property_get_fontVariantCaps", "NDPCanvas_SOURCEGEN")]
    public static partial string GetFontVariantCaps(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_fontVariantCaps", "NDPCanvas_SOURCEGEN")]
    public static partial void SetFontVariantCaps(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_property_get_letterSpacing", "NDPCanvas_SOURCEGEN")]
    public static partial string GetLetterSpacing(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_letterSpacing", "NDPCanvas_SOURCEGEN")]
    public static partial void SetLetterSpacing(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_property_get_textAlign", "NDPCanvas_SOURCEGEN")]
    public static partial string GetTextAlign(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_textAlign", "NDPCanvas_SOURCEGEN")]
    public static partial void SetTextAlign(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_property_get_textBaseline", "NDPCanvas_SOURCEGEN")]
    public static partial string GetTextBaseline(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_textBaseline", "NDPCanvas_SOURCEGEN")]
    public static partial void SetTextBaseline(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_property_get_textRendering", "NDPCanvas_SOURCEGEN")]
    public static partial string GetTextRendering(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_textRendering", "NDPCanvas_SOURCEGEN")]
    public static partial void SetTextRendering(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_property_get_wordSpacing", "NDPCanvas_SOURCEGEN")]
    public static partial string GetWordSpacing(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_wordSpacing", "NDPCanvas_SOURCEGEN")]
    public static partial void SetWordSpacing(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_method_resetTransform", "NDPCanvas_SOURCEGEN")]
    public static partial void ResetTransform(JSObject obj);

    [JSImport("CanvasRenderingContext2D_method_rotate", "NDPCanvas_SOURCEGEN")]
    public static partial void Rotate(JSObject obj, double angle);

    [JSImport("CanvasRenderingContext2D_method_scale", "NDPCanvas_SOURCEGEN")]
    public static partial void Scale(JSObject obj, double x, double y);

    [JSImport("CanvasRenderingContext2D_method_transform", "NDPCanvas_SOURCEGEN")]
    public static partial void Transform(JSObject obj, double a, double b, double c, double d, double e, double f);

    [JSImport("CanvasRenderingContext2D_method_translate", "NDPCanvas_SOURCEGEN")]
    public static partial void Translate(JSObject obj, double x, double y);

    [JSImport("CanvasRenderingContext2D_property_get_fillStyle", "NDPCanvas_SOURCEGEN")]
    public static partial string GetFillStyle(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_fillStyle", "NDPCanvas_SOURCEGEN")]
    public static partial void SetFillStyle(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_property_get_strokeStyle", "NDPCanvas_SOURCEGEN")]
    public static partial string GetStrokeStyle(JSObject obj);
    [JSImport("CanvasRenderingContext2D_property_set_strokeStyle", "NDPCanvas_SOURCEGEN")]
    public static partial void SetStrokeStyle(JSObject obj, string value);

    [JSImport("CanvasRenderingContext2D_method_roundRect", "NDPCanvas_SOURCEGEN")]
    public static partial void RoundRect(JSObject obj, double x, double y, double w, double h);

    [JSImport("CanvasRenderingContext2D_method_roundRect_opt", "NDPCanvas_SOURCEGEN")]
    public static partial void RoundRect(JSObject obj, double x, double y, double w, double h, double radii);

}
