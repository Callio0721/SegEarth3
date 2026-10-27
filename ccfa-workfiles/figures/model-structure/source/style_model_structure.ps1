$ppt = New-Object -ComObject PowerPoint.Application
$src = 'D:\论文\9.27论文\中文论文\绘图\模型结构图.pptx'
$out = 'D:\论文\9.27论文\中文论文\绘图\模型结构图_学术版.pptx'
$preview = 'D:\论文\9.27论文\中文论文\绘图\模型结构图_学术版.png'

$pres = $ppt.Presentations.Open($src, $true, $true, $false)
$pres.SaveCopyAs($out)
$pres.Close()
$pres = $ppt.Presentations.Open($out, $false, $false, $false)
$slide = $pres.Slides.Item(1)

function RGB([int]$r, [int]$g, [int]$b) { return $r + (256 * $g) + (65536 * $b) }
$navy = RGB 24 50 75
$slate = RGB 82 101 119
$line = RGB 126 145 161
$blue = RGB 76 121 166
$blueFill = RGB 232 240 249
$purple = RGB 116 82 166
$purpleFill = RGB 245 237 253
$teal = RGB 43 126 121
$tealFill = RGB 232 247 244
$orange = RGB 194 117 57
$orangeFill = RGB 253 241 229
$paper = RGB 255 255 255
$soft = RGB 248 250 252

function SetTextStyle($sh, $size, $bold = $false, $color = $navy, $font = 'Times New Roman') {
    try {
        $tr = $sh.TextFrame2.TextRange
        $tr.Font.Name = $font
        $tr.Font.Size = $size
        $tr.Font.Bold = $(if ($bold) { -1 } else { 0 })
        $tr.Font.Fill.ForeColor.RGB = $color
    } catch {}
}

function SetLine($sh, $color = $line, $weight = 1.2, $dash = 1) {
    try {
        $sh.Line.Visible = -1
        $sh.Line.ForeColor.RGB = $color
        $sh.Line.Weight = $weight
        $sh.Line.DashStyle = $dash
    } catch {}
}

function SetFill($sh, $color, $trans = 0) {
    try {
        $sh.Fill.Visible = -1
        $sh.Fill.ForeColor.RGB = $color
        $sh.Fill.Transparency = $trans
    } catch {}
}

function WalkStyle($sh, $size = 10, $color = $navy) {
    try {
        if ($sh.HasTextFrame -eq -1 -and $sh.TextFrame2.HasText -eq -1) {
            SetTextStyle $sh $size $false $color
        }
    } catch {}
    if ($sh.Type -eq 6) {
        for ($k = 1; $k -le $sh.GroupItems.Count; $k++) {
            WalkStyle $sh.GroupItems.Item($k) $size $color
        }
    }
}

# Global typography and connector treatment.
for ($i = 1; $i -le $slide.Shapes.Count; $i++) {
    $sh = $slide.Shapes.Item($i)
    WalkStyle $sh 10 $navy
    SetLine $sh $line 1.15 1
}

# Retain the original three-region layout while neutralizing saturated backgrounds.
SetFill $slide.Shapes.Item(1) $paper 0
SetLine $slide.Shapes.Item(1) $navy 1.25 4
SetFill $slide.Shapes.Item(2) $soft 0
SetLine $slide.Shapes.Item(2) $soft 0.1 1
SetFill $slide.Shapes.Item(11) $paper 0
SetLine $slide.Shapes.Item(11) $navy 1.25 4
SetFill $slide.Shapes.Item(12) (RGB 247 251 253) 0
SetLine $slide.Shapes.Item(12) (RGB 247 251 253) 0.1 1

# Hierarchy of section labels.
SetTextStyle $slide.Shapes.Item(7) 17 $true $navy
SetTextStyle $slide.Shapes.Item(21) 16 $true $navy
SetTextStyle $slide.Shapes.Item(24) 16 $true $navy
SetTextStyle $slide.Shapes.Item(23) 15 $true $navy
SetTextStyle $slide.Shapes.Item(4) 10 $false $slate
SetTextStyle $slide.Shapes.Item(5) 12 $true $navy

# Role cards retain their original iconography and positions.
$role = @(
    @{ idx = 8; fill = $purpleFill; edge = $purple },
    @{ idx = 9; fill = $tealFill; edge = $teal },
    @{ idx = 10; fill = $orangeFill; edge = $orange }
)
foreach ($r in $role) {
    $g = $slide.Shapes.Item($r.idx)
    # Keep the original grouped illustrations and their internal fills intact.
    # Only recolor the group's outer outline and its text.
    SetLine $g $r.edge 1.2 1
    for ($k = 1; $k -le $g.GroupItems.Count; $k++) {
        $c = $g.GroupItems.Item($k)
        SetLine $c $r.edge 1.0 1
        try {
            if ($c.HasTextFrame -eq -1 -and $c.TextFrame2.HasText -eq -1) {
                SetTextStyle $c 9.5 $false $r.edge
            }
        } catch {}
    }
}

# Shared profile and method blocks.
SetFill $slide.Shapes.Item(29) $blueFill 0
SetLine $slide.Shapes.Item(29) $blue 1.3 1
SetTextStyle $slide.Shapes.Item(29) 10 $true $navy
SetFill $slide.Shapes.Item(25) $blueFill 0
SetLine $slide.Shapes.Item(25) $navy 1.4 1
SetFill $slide.Shapes.Item(33) $blueFill 0
SetLine $slide.Shapes.Item(33) $blue 1.3 1
SetTextStyle $slide.Shapes.Item(33) 10 $true $navy
SetFill $slide.Shapes.Item(39) $soft 0
SetLine $slide.Shapes.Item(39) $line 1.2 1
SetTextStyle $slide.Shapes.Item(39) 10 $true $navy
SetTextStyle $slide.Shapes.Item(40) 10 $true $navy

# Consistent view labels; the original images remain untouched.
try { $slide.Shapes.Item(15).TextFrame2.TextRange.Text = 'Wide-context view' } catch {}
try { $slide.Shapes.Item(17).TextFrame2.TextRange.Text = 'Local-detail view' } catch {}
try { $slide.Shapes.Item(20).TextFrame2.TextRange.Text = 'Input image' } catch {}
SetTextStyle $slide.Shapes.Item(15) 10 $true $orange
SetTextStyle $slide.Shapes.Item(17) 10 $true $teal
SetTextStyle $slide.Shapes.Item(20) 10 $false $slate

# Make the thin line arrows consistent without changing their positions.
for ($i = 1; $i -le $slide.Shapes.Count; $i++) {
    $sh = $slide.Shapes.Item($i)
    try {
        if ($sh.Type -eq 1 -and $sh.Width -lt 80 -and $sh.Height -lt 5) {
            SetLine $sh $navy 1.4 1
        }
        if ($sh.Type -eq 1 -and $sh.Width -lt 5 -and $sh.Height -gt 20) {
            SetLine $sh $navy 1.4 1
        }
    } catch {}
}

$slide.Export($preview, 'PNG', 2400, 1350)
$pres.Save()
$pres.Close()
$ppt.Quit()
Write-Output $out
Write-Output $preview
