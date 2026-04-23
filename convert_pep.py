import re
from pathlib import Path

def parse_pep(html_content):
    """将 PEP HTML 内容转换为 Markdown 格式"""
    result = []
    
    title_match = re.search(r'<h1 class="page-title">([^<]+)</h1>', html_content)
    if title_match:
        result.append(f"# {title_match.group(1).strip()}")
    
    metadata_pattern = r'<dt class="field-[^>]*">([^<]+)<span class="colon">:</span></dt>\s*<dd class="field-[^>]*">([^<]+(?:</abbr>|[^<])*)</dd>'
    metadata_matches = re.findall(metadata_pattern, html_content)
    
    if metadata_matches:
        result.append("\n**Metadata:**\n")
        for key, value in metadata_matches:
            value = re.sub(r'<[^>]+>', '', value).strip()
            value = value.replace('\n', ' ')
            result.append(f"- **{key}**: {value}")
        result.append("")
    
    content_start = html_content.find('<section id="pep-content">')
    if content_start != -1:
        main_content = html_content[content_start:]
        
        toc_end_match = re.search(r'<hr class="docutils" />', main_content)
        if toc_end_match:
            main_content = main_content[toc_end_match.end():]
        
        main_content = re.sub(r'<details[^>]*>.*?</details>', '', main_content, flags=re.DOTALL)
        
        for i in range(6, 0, -1):
            pattern = rf'<h{i}[^>]*>(.*?)</h{i}>'
            replacement = lambda m, n=i: '#' * n + ' ' + re.sub(r'<[^>]+>', '', m.group(1)).strip() + '\n\n'
            main_content = re.sub(pattern, replacement, main_content, flags=re.DOTALL)
        
        main_content = re.sub(r'<p[^>]*>(.*?)</p>', lambda m: re.sub(r'<[^>]+>', '', m.group(1)).strip() + '\n\n', main_content, flags=re.DOTALL)
        
        main_content = re.sub(r'<li[^>]*>(.*?)</li>', lambda m: '- ' + re.sub(r'<[^>]+>', '', m.group(1)).strip() + '\n', main_content, flags=re.DOTALL)
        
        main_content = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', lambda m: '[' + re.sub(r'<[^>]+>', '', m.group(2)) + '](' + m.group(1) + ')', main_content, flags=re.DOTALL)
        
        main_content = re.sub(r'<strong[^>]*>([^<]+)</strong>', lambda m: '**' + m.group(1) + '**', main_content)
        main_content = re.sub(r'<em[^>]*>([^<]+)</em>', lambda m: '*' + m.group(1) + '*', main_content)
        
        main_content = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: '> ' + re.sub(r'<[^>]+>', '', m.group(1)).strip() + '\n\n', main_content, flags=re.DOTALL)
        
        main_content = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', lambda m: '\n```\n' + m.group(1) + '\n```\n', main_content, flags=re.DOTALL)
        
        main_content = re.sub(r'<[^>]+>', '', main_content)
        
        main_content = re.sub(r'&nbsp;', ' ', main_content)
        main_content = re.sub(r'&amp;', '&', main_content)
        main_content = re.sub(r'&lt;', '<', main_content)
        main_content = re.sub(r'&gt;', '>', main_content)
        main_content = re.sub(r'&quot;', '"', main_content)
        main_content = re.sub(r'&#39;', "'", main_content)
        
        main_content = re.sub(r'[ \t]+', ' ', main_content)
        main_content = re.sub(r'\n{3,}', '\n\n', main_content)
        
        result.append(main_content.strip())
    
    return '\n'.join(result)

def main():
    input_dir = Path('pep_html')
    output_dir = Path('pep_en')
    output_dir.mkdir(exist_ok=True)
    
    pep_files = sorted(input_dir.glob('pep_*.html'))
    print(f"Found {len(pep_files)} PEP files")
    
    success_count = 0
    for file_path in pep_files:
        try:
            content = file_path.read_text(encoding='utf-8')
            num = re.search(r'pep_(\d+)', file_path.name).group(1)
            markdown = parse_pep(content)
            output_file = output_dir / f'PEP {num}.md'
            output_file.write_text(markdown, encoding='utf-8')
            success_count += 1
            print(f"[+] {file_path.name} -> {output_file.name}")
        except Exception as e:
            print(f"[-] Failed: {file_path.name} - {e}")
    
    print(f"\nCompleted: {success_count}/{len(pep_files)} files")

if __name__ == '__main__':
    main()
