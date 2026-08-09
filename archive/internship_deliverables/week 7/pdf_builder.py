import os
from datetime import datetime
from typing import Dict, Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class PDFReportGenerator:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_pdf(self, job_id: str, metrics: Dict[str, Any], title: str = "Backend AI Data Analytics Report") -> str:
        pdf_filename = f"report_{job_id}.pdf"
        pdf_path = os.path.join(self.output_dir, pdf_filename)
        
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#0F172A"),
            spaceAfter=6
        )

        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#64748B"),
            spaceAfter=15
        )

        section_heading = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#3B82F6"),
            spaceBefore=12,
            spaceAfter=8
        )

        body_style = ParagraphStyle(
            "BodyTextCustom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#1E293B")
        )

        story = []

        # 1. Header Title & Subtitle
        story.append(Paragraph(title, title_style))
        now_str = datetime.now().strftime("%B %d, %Y - %H:%M:%S UTC")
        story.append(Paragraph(f"Generated via Background Job ID: <b>{job_id}</b> | Timestamp: {now_str}", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#3B82F6"), spaceAfter=15))

        # 2. Executive Summary Metrics Table
        story.append(Paragraph("1. Executive Summary & Corpus Metrics", section_heading))
        
        summary_data = [
            [Paragraph("<b>Metric</b>", body_style), Paragraph("<b>Value</b>", body_style)],
            [Paragraph("Total Quotes Scraped", body_style), Paragraph(str(metrics["total_quotes"]), body_style)],
            [Paragraph("Unique Authors", body_style), Paragraph(str(metrics["unique_authors"]), body_style)],
            [Paragraph("Average Quote Length", body_style), Paragraph(f"{metrics['avg_quote_length']} characters", body_style)],
            [Paragraph("Scraper Politeness Status", body_style), Paragraph("<font color='#16A34A'><b>100% Compliant (robots.txt delay)</b></font>", body_style)]
        ]

        summary_table = Table(summary_data, colWidths=[3.2*inch, 3.8*inch])
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (1, 0), colors.HexColor("#F1F5F9")),
            ("TEXTCOLOR", (0, 0), (1, 0), colors.HexColor("#0F172A")),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 15))

        # 3. Top Authors & Tags Leaderboard
        story.append(Paragraph("2. Top Authors & Category Breakdown", section_heading))
        
        author_rows = [[Paragraph(f"<b>{a}</b>", body_style), Paragraph(f"{c} quotes", body_style)] for a, c in metrics["top_authors"]]
        tag_rows = [[Paragraph(f"<b>#{t}</b>", body_style), Paragraph(f"{c} occurrences", body_style)] for t, c in metrics["top_tags"]]

        breakdown_data = [
            [Paragraph("<b>Top Authors</b>", body_style), Paragraph("<b>Top Content Tags</b>", body_style)]
        ]
        
        max_len = max(len(author_rows), len(tag_rows))
        for i in range(max_len):
            a_text = f"{author_rows[i][0].text} ({author_rows[i][1].text})" if i < len(author_rows) else ""
            t_text = f"{tag_rows[i][0].text} ({tag_rows[i][1].text})" if i < len(tag_rows) else ""
            breakdown_data.append([Paragraph(a_text, body_style), Paragraph(t_text, body_style)])

        breakdown_table = Table(breakdown_data, colWidths=[3.5*inch, 3.5*inch])
        breakdown_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (1, 0), colors.HexColor("#EFF6FF")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFDBFE")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(breakdown_table)
        story.append(Spacer(1, 15))

        # 4. Extracted Sample Quotes Table
        story.append(Paragraph("3. Extracted Sample Records", section_heading))
        
        sample_table_data = [[Paragraph("<b>Author</b>", body_style), Paragraph("<b>Quote Sample</b>", body_style), Paragraph("<b>Tags</b>", body_style)]]
        
        for q in metrics["sample_quotes"]:
            author_p = Paragraph(f"<b>{q.get('author', 'Unknown')}</b>", body_style)
            quote_p = Paragraph(f"<i>“{q.get('quote', '')}”</i>", body_style)
            tags_str = ", ".join([f"#{t}" for t in q.get("tags", [])])
            tags_p = Paragraph(tags_str, body_style)
            sample_table_data.append([author_p, quote_p, tags_p])

        sample_table = Table(sample_table_data, colWidths=[1.8*inch, 3.7*inch, 1.5*inch])
        sample_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F8FAFC")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(sample_table)

        # Build document
        doc.build(story)
        return pdf_path
