import re

src = r"C:\Users\点拨\Desktop\常用模板\陈婉君\陈婉君_AI作品集_编辑版.html"
out = r"D:\1\香港四大实习2027\portfolio_deploy\index.html"

with open(src, encoding="utf-8") as f:
    html = f.read()

# 1) 删除编辑工具条（editbar 整块：面板 + 悬浮圆点）
start = html.find('<div id="editbar">')
end_marker = '<button class="eb-fab" id="ebFab" title="对内编辑">✏️</button>'
ei = html.find(end_marker)
if start != -1 and ei != -1:
    end = html.find('</div>', ei) + len('</div>')
    line_start = html.rfind('\n', 0, start) + 1
    html = html[:line_start] + html[end:].lstrip('\n')

# 2) 删除所有脚本
html = re.sub(r'<script>.*?</script>', '', html, flags=re.S)

# 3) 删除 contenteditable 属性
html = re.sub(r'\s*contenteditable="[^"]*"', '', html)

# 4) 清理截图位上传控件
html = re.sub(r'<input type="file"[^>]*>', '', html)
html = re.sub(r'<div class="shot-actions">.*?</div>', '', html, flags=re.S)
html = re.sub(r'\s*data-upload-ready="[^"]*"', '', html)
html = re.sub(r'\s*data-placeholder="[^"]*"', '', html)

# 5) footer 去掉「AI 产品」+ 标题同步
html = html.replace('© 陈婉君 · AI 产品作品集', '© 陈婉君 · 作品集')
html = html.replace('<title>陈婉君 · AI 产品作品集</title>', '<title>陈婉君 · 作品集</title>')

# 6) 删除编辑相关 CSS
html = re.sub(r'\n\s*/\* 可编辑区块[^*]*\*/', '\n', html)
html = re.sub(r'\s*\[contenteditable="true"\]\{[^}]*\}', '', html)
html = re.sub(r'\s*\[contenteditable="true"\]:hover\{[^}]*\}', '', html)
html = re.sub(r'\s*\[contenteditable="true"\]:focus\{[^}]*\}', '', html)
html = re.sub(r'\n\s*/\* 对内编辑工具条[^*]*\*/.*?body\.editing \[contenteditable\]\{[^}]*\}', '', html, flags=re.S)
html = re.sub(r'\s*\.shot-actions\{[^}]*\}', '', html)
html = re.sub(r'\s*\.shot:hover \.shot-actions\{[^}]*\}', '', html)
html = re.sub(r'\s*\.shot-btn\{[^}]*\}', '', html)
html = re.sub(r'\s*\.shot-btn:hover\{[^}]*\}', '', html)
html = re.sub(r'\s*\.shot\.dragover\{[^}]*\}', '', html)

# 7) 补一个可见的「对外链接」区块（在 footer 之前）
external_section = '''<!-- ============ 对外链接 ============ -->
<section id="external">
  <div class="wrap">
    <div class="eyebrow">Public Link</div>
    <h2>对外链接</h2>
    <p class="sub">这是可发送给 HR / 面试官的固定对外链接，内容随作品集更新而更新。</p>
    <div class="locked-card">
      <div>
        <div class="lbl">AI 作品集 · 对外展示</div>
        <div class="url">https://506675124-chen.github.io/chenwanjun-ai-portfolio/</div>
      </div>
      <div class="lock">🔒 只读 · 不可编辑</div>
    </div>
  </div>
</section>

'''
html = html.replace('<footer>', external_section + '<footer>', 1)

with open(out, "w", encoding="utf-8") as f:
    f.write(html)

# 自检
checks = {
    'script': html.count('<script'),
    'editbar': html.count('id="editbar"'),
    'ebFab': html.count('ebFab'),
    'contenteditable': html.count('contenteditable'),
    'shot-actions': html.count('shot-actions'),
    'data-upload-ready': html.count('data-upload-ready'),
    'AI 产品 in footer/title': html.count('AI 产品作品集'),
    'external section': html.count('id="external"'),
    'public url present': html.count('506675124-chen.github.io/chenwanjun-ai-portfolio'),
}
print("OUTPUT BYTES:", len(html.encode('utf-8')))
print(checks)
