from arxiv2text import arxiv_to_text
import re


def process_pdf(pdf_url, sections_to_extract):
    # PDF에서 텍스트 추출
    extracted_text = arxiv_to_text(pdf_url)

    def extract_text_before_references(text):
        pattern = re.compile(r"\n(?:references)", re.IGNORECASE)
        match = pattern.search(text)
        return text[: match.start()].strip() if match else text.strip()

    def extract_sections(text, sections):
        extracted_text = {}
        for section in sections:
            pattern = rf"{section}\s*\n(.*?)\n\n"
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                content = match.group(1).strip()
                extracted_text[section] = content
            else:
                extracted_text[section] = f"{section} 섹션을 찾을 수 없습니다."
        return extracted_text

    # 참조 이전의 텍스트 추출
    text_before_references = extract_text_before_references(extracted_text)

    # 섹션 추출
    result = extract_sections(text_before_references, sections_to_extract)

    # inputs 리스트 생성
    inputs = [f"{section}:{content}" for section, content in result.items()]

    return inputs


if __name__ == "__main__":
    pdf_url = "https://proceedings.neurips.cc/paper_files/paper/2021/file/854d9fca60b4bd07f9bb215d59ef5561-Paper.pdf"
    sections_to_extract = ["Abstract", "Results", "Conclusion"]

    inputs = process_pdf(pdf_url, sections_to_extract)
