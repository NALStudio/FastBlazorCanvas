using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices.JavaScript;
using System.Runtime.Versioning;
using System.Security.Claims;
using System.Text;
using System.Threading.Tasks;

namespace NDiscoPlus.Canvas;

[SupportedOSPlatform("browser")]
internal static class CanvasManager
{
    private static Task? loadingTask;

    public static async ValueTask LoadJsModule()
    {
        loadingTask ??= InternalLoadJsModule();
        if (!loadingTask.IsCompleted)
            await loadingTask;
    }

    private static async Task InternalLoadJsModule()
    {
        await JSHost.ImportAsync("NDPCanvas_CORE", "./ndpcanvas_core.js");
        await JSHost.ImportAsync("NDPCanvas_SOURCEGEN", "./ndpcanvas_sourcegen.g.js");
    }
}
