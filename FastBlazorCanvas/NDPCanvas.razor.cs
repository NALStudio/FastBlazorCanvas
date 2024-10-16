using Microsoft.AspNetCore.Components;
using NDiscoPlus.Canvas.Context2D;
using System.Diagnostics;
using System.Runtime.Versioning;

namespace NDiscoPlus.Canvas;

[SupportedOSPlatform("browser")]
public partial class NDPCanvas
{
    private ElementReference? canvasRef;

    #region Component Lifecycle
    private readonly TaskCompletionSource waitForFirstRender = new();
    protected override void OnAfterRender(bool firstRender)
    {
        if (firstRender)
            waitForFirstRender.SetResult();
    }

    protected override async Task OnInitializedAsync()
    {
        await CanvasManager.LoadJsModule();
    }
    #endregion

    public async Task<CanvasRenderingContext2D> GetContextAsync()
    {
        await waitForFirstRender.Task;
        Debug.Assert(canvasRef.HasValue);
    }
}