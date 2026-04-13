# -*- coding: utf-8 -*-
"""
风叔知识库提取脚本（轻量版）
只提取最近30篇文章的标题和关键段落，避免全量解析导致太慢
"""
import pdfplumber, docx, os, sys, re
from datetime import datetime
import logging
import warnings

warnings.filterwarnings('ignore')
logging.getLogger('pdfminer').setLevel(logging.ERROR)

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr = open(os.devnull, 'w')  # 抑制所有stderr

KNOWLEDGE_BASE = r'E:\记忆承载'

def extract_pdf_first_pages(path, max_pages=2):
    texts = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages[:max_pages]:
                t = page.extract_text()
                if t and len(t.strip()) > 20:
                    texts.append(t)
    except:
        pass
    return '\n'.join(texts)

def extract_docx_first_part(path, max_chars=2000):
    try:
        doc = docx.Document(path)
        parts = []
        total = 0
        for p in doc.paragraphs:
            if p.text.strip():
                parts.append(p.text)
                total += len(p.text)
                if total > max_chars:
                    break
        return '\n'.join(parts)
    except:
        return ''

def extract_file(path):
    if path.lower().endswith('.pdf'):
        return extract_pdf_first_pages(path)
    elif path.lower().endswith(('.docx', '.doc')):
        return extract_docx_first_part(path)
    return ''

def clean_text(text):
    text = re.sub(r'加微信号\w+，免费进资料群', '', text)
    text = re.sub(r'知识星球TOP资源群.*?入群', '', text, flags=re.DOTALL)
    text = re.sub(r'VIP 群:.*?免费群:.*?分发', '', text, flags=re.DOTALL)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def get_title(fn):
    title = re.sub(r'^\d{4,8}[-_]?', '', fn)
    title = re.sub(r'^记忆承载\d*[-_]?', '', title)
    title = re.sub(r'^（付费文）[：:]?', '', title)
    title = re.sub(r'^（付费）[：:]?', '', title)
    title = re.sub(r'\.(pdf|docx|doc)$', '', title, flags=re.IGNORECASE)
    return title.strip()

def get_date_from_filename(fn):
    """从文件名提取日期用于排序"""
    m = re.match(r'(\d{4,8})', fn)
    if m:
        d = m.group(1)
        if len(d) == 8:
            return d
        elif len(d) == 6:
            return d + '00'
        return d + '0000'
    return '00000000'

def main():
    files = []
    
    for root, dirs, filenames in os.walk(KNOWLEDGE_BASE):
        if 'PDF版本' in root:
            continue
        for fn in filenames:
            if not fn.lower().endswith(('.pdf', '.docx')):
                continue
            fp = os.path.join(root, fn)
            files.append((fp, fn))
    
    # 按日期排序（最新的在后面）
    files.sort(key=lambda x: get_date_from_filename(x[1]))
    
    # 只取最近60篇
    recent = files[-60:] if len(files) > 60 else files
    
    print(f"=== 风叔知识库 ({len(files)}篇总量，展示最近{len(recent)}篇) ===\n")
    
    for fp, fn in recent:
        title = get_title(fn)
        text = extract_file(fp)
        text = clean_text(text)
        
        if not text or len(text) < 50:
            continue
        
        # 取前500字作为摘要
        summary = text[:500] + ('...' if len(text) > 500 else '')
        
        print(f"### {title}")
        print(f"{summary}")
        print()
    
    # 核心思想摘要
    print("=== 风叔核心思想摘要 ===")
    print("""
**【树与路】** 人类有两种"懂"——探树（收集知识元素）和探路（走通一条路径）。大多数人一辈子在探树，只有探路才能提升认知。认知是习出来的，不是学出来的。值钱的不是知识本身，而是知识的排列组合形成的"路"。

**【吃鸡策略】** 不必当那只等了364天饲料的火鸡，也可以选择吃那只鸡。用极少的本金、极小的风险，去博取极端事件（感恩节）的超大收益。与塔勒布的杠铃策略相通：90%保护本金，10%去搏爆炸增长。

**【信息价值】** 从宋江身上学到：一个人即使毫无硬实力，只要善于利用信息——收集、处理、交换——就能在社会中生存乃至游刃有余。职场中对老板的价值，不只是干活，更是信息价值和耳目价值。

**【矫情才是障碍】** 弱小和无知不是生存的障碍，矫情才是。矫情是真实感受和认知判断的错配——2%的第一印象占据98%的判断。AI时代，只有非标、多元的能力才能生存。

**【世界格局】** 二战后美国构建的安全体系正在瓦解，世界回到列强博弈模式。安全成本抬升将深刻影响每个人。美元体系面临特里芬悖论，硬资产（矿产、能源）价值重估。

**【人生观】** 人生如看电影，曲终人散是注定的，关键是过程中的体验和出离感。人生没有标准意义，意义是自己赋予的。目标是可考核的，欲望不是——大多数人口口声声的目标，其实只是欲望。
""")

if __name__ == '__main__':
    main()
