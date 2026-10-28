param(
    [ValidateSet('Simple','Changelog','Plain','Images','Atoms')][string]$Mode = 'Simple',
    [string]$InputPath = 'D:\MAA-Arknights-Assistant\data\CHANGELOG.md',
    [string]$FontFamily = 'Microsoft YaHei, Global User Interface',
    [ValidateSet('Ideal','Display')][string]$FormattingMode = 'Ideal',
    [switch]$UseMaaNative,
    [string]$Culture = 'zh-CN',
    [switch]$DisableLazyLoad,
    [switch]$UseMarkdownControl,
    [double[]]$Widths = @(560,540,580),
    [switch]$SkipScrolling
)
$ErrorActionPreference = 'Stop'
# Isolated diagnostic process: never starts MAA or changes its files.
Add-Type -TypeDefinition @'
using System.Runtime.InteropServices;
public static class ProbeErrorMode {
    [DllImport("kernel32.dll")] public static extern uint SetErrorMode(uint mode);
}
'@
[void][ProbeErrorMode]::SetErrorMode(0x8003)
$dep = 'D:\MAA-Arknights-Assistant\externals'
$env:PATH = $dep + ';' + $env:PATH
if ($UseMaaNative) {
    foreach ($nativeName in @('wpfgfx_cor3.dll','PresentationNative_cor3.dll')) {
        $nativeHandle = [Runtime.InteropServices.NativeLibrary]::Load((Join-Path $dep $nativeName))
        Write-Output "PRELOADED $nativeName"
    }
}
foreach ($name in @('WindowsBase','System.Xaml','PresentationCore','PresentationFramework','MdXaml.Plugins','MdXaml','HtmlAgilityPack','MdXaml.Html')) {
    [void][Reflection.Assembly]::LoadFrom((Join-Path $dep ($name + '.dll')))
}
[System.Windows.Media.RenderOptions]::ProcessRenderMode = [System.Windows.Interop.RenderMode]::SoftwareOnly
if ($Culture) {
    [Threading.Thread]::CurrentThread.CurrentCulture = [Globalization.CultureInfo]::GetCultureInfo($Culture)
    [Threading.Thread]::CurrentThread.CurrentUICulture = [Globalization.CultureInfo]::GetCultureInfo($Culture)
    [Windows.FrameworkElement]::LanguageProperty.OverrideMetadata([Windows.FrameworkElement], [Windows.FrameworkPropertyMetadata]::new([Windows.Markup.XmlLanguage]::GetLanguage($Culture)))
}
$renderer = [MdXaml.Markdown]::new()
$renderer.DisabledLazyLoad = $DisableLazyLoad.IsPresent
$renderer.AssetPathRoot = 'D:\MAA-Arknights-Assistant'
$plugins = [MdXaml.Plugins.MdXamlPlugins]::new()
$plugins.Setups.Add([MdXaml.Html.HtmlPluginSetup]::new())
$renderer.Plugins = $plugins
$styleXml = [IO.File]::ReadAllText((Join-Path $PSScriptRoot 'MdXaml.upstream.xaml'))
$resources = [Windows.Markup.XamlReader]::Parse($styleXml)
$renderer.DocumentStyle = $resources['MdXamlStyle']
$raw = [IO.File]::ReadAllText($InputPath)
if ($Mode -eq 'Simple') { $raw = "# 排版测试`n`n中文和 English 测试段落。`n`n- 自动战斗`n- 更新日志" }
if ($Mode -in @('Images','Atoms')) {
    $raw = [regex]::Replace($raw, '([^\[`]|^)@([^\s]+)', [Text.RegularExpressions.MatchEvaluator]{
        param($m)
        $userName = $m.Groups[2].Value
        $prefix = ''
        if ($userName -match '^[a-zA-Z0-9-]+$') {
            $avatarFile = Join-Path 'D:/MAA-Arknights-Assistant/cache/contributor' ($userName + '.png')
            if (!(Test-Path -LiteralPath $avatarFile)) { $avatarFile = 'D:/MAA-Arknights-Assistant/cache/contributor/_placeholder.png' }
            if (Test-Path -LiteralPath $avatarFile) { $prefix = '![avatar](' + $avatarFile + ' "' + $userName + '"){width=16px height=16px}' + [char]0x2060 }
        }
        return $m.Groups[1].Value + $prefix + '[@' + $userName + '](https://github.com/' + $userName + ')'
    })
}
Write-Output "START mode=$Mode runtime=$([Environment]::Version) apartment=$([Threading.Thread]::CurrentThread.ApartmentState)"
if ($Mode -eq 'Plain') {
    $doc = [Windows.Documents.FlowDocument]::new()
    $doc.Blocks.Add([Windows.Documents.Paragraph]::new([Windows.Documents.Run]::new($raw)))
} elseif ($UseMarkdownControl) {
    $viewer = [MdXaml.MarkdownScrollViewer]::new()
    $viewer.Plugins = $plugins
    $viewer.MarkdownStyle = $resources['MdXamlStyle']
    $viewer.Engine.DisabledLazyLoad = $DisableLazyLoad.IsPresent
    $viewer.Markdown = $raw.Replace('<details open>','<details open="true">')
    $doc = $viewer.Document
} else {
    $doc = $renderer.Transform($raw.Replace('<details open>','<details open="true">'))
}
Write-Output 'PARSED'
$doc.FontFamily = [Windows.Media.FontFamily]::new($FontFamily)
[Windows.Media.TextOptions]::SetTextFormattingMode($doc, [Windows.Media.TextFormattingMode]::$FormattingMode)
function Get-ProbeParagraphs($blocks) {
    foreach ($block in $blocks) {
        if ($block -is [Windows.Documents.Paragraph]) { Write-Output $block }
        elseif ($block -is [Windows.Documents.Section]) { Get-ProbeParagraphs $block.Blocks }
        elseif ($block -is [Windows.Documents.List]) { foreach ($item in $block.ListItems) { Get-ProbeParagraphs $item.Blocks } }
        elseif ($block -is [Windows.Documents.Table]) {
            foreach ($group in $block.RowGroups) { foreach ($row in $group.Rows) { foreach ($cell in $row.Cells) { Get-ProbeParagraphs $cell.Blocks } } }
        }
        elseif ($block -is [Windows.Documents.BlockUIContainer] -and $block.Child -is [Windows.Controls.Expander] -and $block.Child.Content -is [Windows.Controls.FlowDocumentScrollViewer]) {
            Get-ProbeParagraphs $block.Child.Content.Document.Blocks
        }
    }
}
if ($Mode -eq 'Atoms') {
    $merged = 0
    $paragraphs = @(Get-ProbeParagraphs $doc.Blocks)
    Write-Output ("PARAGRAPHS count=" + $paragraphs.Count + " image-markdown=" + ([regex]::Matches($raw,'!\[avatar\]').Count))
    foreach ($paragraph in $paragraphs) {
        $inlines = $paragraph.Inlines
        $inline = $inlines.FirstInline
        while ($null -ne $inline) {
            $cursor = $inline.NextInline
            if ($inline -is [Windows.Documents.InlineUIContainer] -and $cursor -is [Windows.Documents.Run] -and $cursor.Text -eq [string][char]0x2060) {
                $joiner = $cursor
                $cursor = $joiner.NextInline
                if ($cursor -is [Windows.Documents.Hyperlink] -and $cursor.Inlines.FirstInline -is [Windows.Documents.Run] -and $cursor.Inlines.FirstInline.Text.StartsWith('@')) {
                    $link = $cursor
                    $after = $link.NextInline
                    $nameText = [Windows.Controls.TextBlock]::new()
                    $nameText.FontFamily = $doc.FontFamily
                    $nameText.FontSize = $doc.FontSize
                    $atom = [Windows.Documents.InlineUIContainer]::new($nameText)
                    $inlines.InsertBefore($inline, $atom)
                    [void]$inlines.Remove($joiner)
                    [void]$inlines.Remove($inline)
                    [void]$inlines.Remove($link)
                    $nameText.Inlines.Add($inline)
                    $nameText.Inlines.Add($link)
                    $link.TextDecorations = $null
                    $inline = $after
                    $merged++
                    continue
                }
            }
            $inline = $cursor
        }
    }
    Write-Output "MERGED count=$merged"
}
if (!$UseMarkdownControl) {
    $viewer = [Windows.Controls.FlowDocumentScrollViewer]::new()
    $viewer.Document = $doc
}
$root = [Windows.Controls.ScrollViewer]::new()
$root.HorizontalScrollBarVisibility = [Windows.Controls.ScrollBarVisibility]::Disabled
$root.VerticalScrollBarVisibility = [Windows.Controls.ScrollBarVisibility]::Auto
$root.Content = $viewer
foreach ($width in $Widths) {
    $root.Measure([Windows.Size]::new($width,450))
    $root.Arrange([Windows.Rect]::new(0,0,$width,450))
    $root.UpdateLayout()
    $bitmap = [Windows.Media.Imaging.RenderTargetBitmap]::new($width,450,96,96,[Windows.Media.PixelFormats]::Pbgra32)
    $bitmap.Render($root)
    [void]$root.Dispatcher.Invoke([Windows.Threading.DispatcherPriority]::ApplicationIdle, [Action]{})
    Write-Output "RENDERED width=$width height=$($viewer.ActualHeight) scroll=$($root.ScrollableHeight) font=$FontFamily format=$FormattingMode"
    for ($offset = 0; !$SkipScrolling -and $offset -le $root.ScrollableHeight + 450; $offset += 450) {
        $root.ScrollToVerticalOffset($offset)
        $root.UpdateLayout()
        $bitmap.Render($root)
        [void]$root.Dispatcher.Invoke([Windows.Threading.DispatcherPriority]::ApplicationIdle, [Action]{})
    }
}
Get-Process -Id $PID | ForEach-Object { $_.Modules } | Where-Object ModuleName -match 'PresentationNative|wpfgfx|dwrite|TextShap' | ForEach-Object { Write-Output ("MODULE " + $_.ModuleName + ' ' + $_.FileName + ' ' + $_.FileVersionInfo.FileVersion) }
Write-Output 'PASS'
