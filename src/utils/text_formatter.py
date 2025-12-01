def reconstruct_text(words: list[dict],
                     line_thresh: int = 10,
                     para_thresh: int = 25,
                     column_gap_thresh: int = 50,
                     space_per_10px: int = 1) -> str:
    """
    Reconstruct text from OCR word list, preserving layout including lines, paragraphs, columns, and basic tables.

    Args:
        words: list of dicts with keys: 'text', 'left', 'top', 'width', 'height'
        line_thresh: max vertical distance to group words into same line
        para_thresh: vertical gap to consider paragraph break
        column_gap_thresh: min horizontal gap to detect column separation
        space_per_10px: spaces per 10px horizontal gap

    Returns:
        Reconstructed text as string
    """
    if not words:
        return ""

    # Sort words top-to-bottom
    words = sorted(words, key=lambda w: (w['top'], w['left']))

    # Step 1: Group words into lines
    lines = []
    line = []
    line_top = None
    for w in words:
        if line_top is None or abs(w['top'] - line_top) <= line_thresh:
            line.append(w)
            line_top = line_top or w['top']
        else:
            lines.append(line)
            line = [w]
            line_top = w['top']
    if line:
        lines.append(line)

    # Step 2: Detect columns within each line
    output_text = ""
    prev_line_bottom = None

    for line in lines:
        # Sort words in line by left
        line.sort(key=lambda w: w['left'])

        # Paragraph detection
        if prev_line_bottom is not None:
            vertical_gap = line[0]['top'] - prev_line_bottom
            if vertical_gap > para_thresh:
                output_text += "\n"

        # Optional: detect column gaps (basic)
        prev_right = None
        for i, w in enumerate(line):
            if prev_right is not None:
                gap = w['left'] - prev_right
                if gap > column_gap_thresh:
                    # Likely new column / table cell → add extra spaces
                    extra_spaces = 4  # you can tune this
                    output_text += " " * extra_spaces
                else:
                    # Regular space proportional to horizontal gap
                    spaces = max(1, round(gap / 10) * space_per_10px)
                    output_text += " " * spaces
            output_text += w['text']
            prev_right = w['left'] + w['width']

        output_text += "\n"
        prev_line_bottom = max(w['top'] + w['height'] for w in line)

    return output_text.strip()
