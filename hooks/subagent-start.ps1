# 배포판(Subagents) 의 Codex·Antigravity(agy) 서브에이전트 시작 훅. Claude Code 는 플러그인 훅(plugins/<이름>/hooks/)이 같은 일을 한다.
#   Codex: ~/.codex/hooks.json 의 SubagentStart 가 -Harness codex 로 부른다(matcher = 설치한 이름, additionalContextLimit 8000 — AGENTS.md).
#          입력 agent_type = codex/agents/<이름>.toml 의 name.
#   agy:   agy/agents/<이름>/hooks.json 의 SessionStart 가 -Harness agy -Agent <이름> 으로 부른다(agy 는 훅 입력에 에이전트 이름이 없음).
#          에이전트별 훅이라 그 서브에이전트 대화가 시작될 때 한 번만 돈다 — 메인 대화에는 안 돈다(2026-11-25 agy 1.5.16 실측).
#          전역 SessionStart 는 서브에이전트 대화에도 돌아 메인과 가를 수 없지만, 에이전트별 훅에는 그 문제가 없다.
# 넣는 것: 에이전트 파일의 안내(파일 위치·메모리 규칙) + 공통 계약·본문(플러그인 훅 inject-agent-context.ps1 을 그대로 씀) + 에이전트 메모리 목록.
# 메모리 폴더는 Claude Code 와 같은 ~/.claude/agent-memory/<이름>-<이름>/ — 세 하네스가 한 폴더를 쓴다.
# 이 저장소 밖의 서브에이전트(다른 이름)는 건드리지 않는다.
param([ValidateSet('codex', 'agy')][string]$Harness, [string]$Agent)
$ErrorActionPreference = 'Stop'
$utf8 = [System.Text.UTF8Encoding]::new($false)
$hookInput = [System.IO.StreamReader]::new([Console]::OpenStandardInput(), $utf8).ReadToEnd() | ConvertFrom-Json
[Console]::OutputEncoding = $utf8
$none = if ($Harness -eq 'agy') { '{}' } else { '' }

$name = if ($Harness -eq 'agy') { $Agent } else { [string]$hookInput.agent_type }
$plugin = Join-Path (Split-Path $PSScriptRoot -Parent) "plugins\$name"
if ($name -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]*$' -or -not (Test-Path -LiteralPath (Join-Path $plugin "$name\AGENT.md") -PathType Leaf)) {
    [Console]::Out.Write($none); exit 0
}

# 1. 에이전트 파일의 안내 — Claude Code 에서는 에이전트 파일 본문이 시스템 프롬프트라 따로 넣지 않는다
$shell = [System.IO.File]::ReadAllText((Join-Path $plugin "agents\$name.md"), $utf8)
$guide = ($shell -split '(?m)^---\s*$', 3)[2].Trim().Replace('${CLAUDE_PLUGIN_ROOT}', $plugin)

# 2. 공통 계약 + 본문 — 플러그인 훅을 플러그인 위치와 함께 부른다(Claude Code 가 주는 CLAUDE_PLUGIN_ROOT 를 여기서 준다)
$env:CLAUDE_PLUGIN_ROOT = $plugin
$psi = [System.Diagnostics.ProcessStartInfo]::new('powershell.exe', "-NoProfile -ExecutionPolicy Bypass -File `"$(Join-Path $plugin 'hooks\inject-agent-context.ps1')`"")
$psi.RedirectStandardInput = $true; $psi.RedirectStandardOutput = $true; $psi.RedirectStandardError = $true; $psi.UseShellExecute = $false
$psi.StandardOutputEncoding = $utf8; $psi.StandardErrorEncoding = $utf8
$p = [System.Diagnostics.Process]::Start($psi)
$w = [System.IO.StreamWriter]::new($p.StandardInput.BaseStream, $utf8); $w.Write((@{ agent_type = "${name}:$name" } | ConvertTo-Json -Compress)); $w.Close()
$out = $p.StandardOutput.ReadToEnd(); $err = $p.StandardError.ReadToEnd(); $p.WaitForExit()
if ($p.ExitCode -ne 0) { [Console]::Error.Write($err); exit $p.ExitCode }
$context = [string]($out | ConvertFrom-Json).hookSpecificOutput.additionalContext

# 3. 에이전트 메모리 — Claude Code 와 같은 폴더
$memdir = Join-Path $env:USERPROFILE ".claude\agent-memory\$name-$name"
$l0 = Join-Path $memdir 'MEMORY.md'
$index = if (Test-Path -LiteralPath $l0 -PathType Leaf) { [System.IO.File]::ReadAllText($l0, $utf8) } else { '(아직 없음 — 처음 기록할 때 이 폴더와 MEMORY.md 를 만든다)' }
$memory = "# Agent memory`n`nMemory directory: $($memdir.Replace('\', '/')) (Claude Code 와 같은 폴더 — 위 「메모리」 규칙대로 기록)`n`n$index"

$text = @($guide, $context, $memory) -join "`n`n---`n`n"
if ($Harness -eq 'agy') {
    [Console]::Out.Write((@{ injectSteps = @(@{ systemMessage = @{ systemMessage = $text } }) } | ConvertTo-Json -Depth 6 -Compress))
} else {
    [Console]::Out.Write((@{ hookSpecificOutput = @{ hookEventName = 'SubagentStart'; additionalContext = $text } } | ConvertTo-Json -Depth 5 -Compress))
}
