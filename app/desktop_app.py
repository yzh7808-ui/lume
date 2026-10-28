import sys
from typing import Any

import httpx
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt

API_BASE_URL = "http://localhost:8000/api/v1"
USER_ID = "u_001"


class LumeWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Lume")
        self.resize(1200, 860)
        self.setMinimumSize(980, 700)
        self.setStyleSheet(
            """
            QWidget {
                background: #f6f3ee;
                color: #1f2937;
                font-family: "SF Pro Display", "Segoe UI", sans-serif;
            }
            QLabel {
                color: #1f2937;
            }
            QLineEdit, QTextEdit {
                background: #f7f3ef;
                color: #1f2937;
                border: 1px solid #2d2d2d;
                border-radius: 12px;
                padding: 10px 12px;
                font-size: 18px;
            }
            QTextEdit {
                min-height: 110px;
            }
            QPushButton {
                background: #f2f0ec;
                color: #1f2937;
                border: 1px solid #2d2d2d;
                border-radius: 12px;
                padding: 10px 18px;
                font-size: 18px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #eae4dc;
            }
            QPushButton:pressed {
                background: #e1d9d0;
            }
            QListWidget {
                background: transparent;
                border: none;
                color: #1f2937;
                font-size: 17px;
            }
            """
        )

        self.central = QWidget()
        self.setCentralWidget(self.central)

        root = QVBoxLayout(self.central)
        root.setContentsMargins(28, 20, 28, 28)
        root.setSpacing(18)

        browser_row = QHBoxLayout()
        browser_row.setContentsMargins(0, 0, 0, 0)
        browser_row.setSpacing(12)

        for color in ("#ef6a5c", "#f4d35e", "#65c468"):
            dot = QWidget()
            dot.setFixedSize(14, 14)
            dot.setStyleSheet(f"background: {color}; border-radius: 7px;")
            browser_row.addWidget(dot)
        browser_row.addStretch(1)
        root.addLayout(browser_row)

        nav = QLabel("HomeNotesSearchReflection")
        nav.setStyleSheet("font-size: 18px; color: #1f2937; font-weight: 500;")
        root.addWidget(nav)

        title = QLabel("New thought")
        title.setStyleSheet("font-size: 52px; font-weight: 700; letter-spacing: -1.5px;")
        root.addWidget(title)

        form_row = QHBoxLayout()
        form_row.setSpacing(18)

        title_col = QVBoxLayout()
        title_label = QLabel("Title")
        title_label.setStyleSheet("font-size: 18px; font-weight: 500;")
        self.title_input = QLineEdit()
        self.title_input.setFixedHeight(52)
        title_col.addWidget(title_label)
        title_col.addWidget(self.title_input)

        text_col = QVBoxLayout()
        self.content_input = QTextEdit()
        self.content_input.setFixedHeight(110)
        self.content_input.setPlaceholderText("Write down your latest idea, reflection, or insight...")
        text_col.addWidget(self.content_input)

        action_col = QVBoxLayout()
        self.tags_input = QLineEdit()
        self.tags_input.setFixedHeight(52)
        self.tags_input.setPlaceholderText("Tags (comma separated)")
        self.save_button = QPushButton("Save thought")
        self.save_button.setFixedHeight(52)
        self.save_button.clicked.connect(self.save_note)
        action_col.addWidget(self.tags_input)
        action_col.addWidget(self.save_button)

        form_row.addLayout(title_col, 1)
        form_row.addLayout(text_col, 3)
        form_row.addLayout(action_col, 2)
        root.addLayout(form_row)

        weekly_title = QLabel("Weekly reflection")
        weekly_title.setStyleSheet("font-size: 42px; font-weight: 700; letter-spacing: -1.1px;")
        root.addWidget(weekly_title)

        self.weekly_summary = QLabel("Loading weekly reflection...")
        self.weekly_summary.setWordWrap(True)
        self.weekly_summary.setStyleSheet("font-size: 18px; color: #2f3746;")
        root.addWidget(self.weekly_summary)

        self.weekly_tags = QLabel("")
        self.weekly_tags.setStyleSheet("font-size: 18px; color: #1f2937; opacity: 0.9;")
        root.addWidget(self.weekly_tags)

        self.weekly_questions = QLabel("")
        self.weekly_questions.setWordWrap(True)
        self.weekly_questions.setStyleSheet("font-size: 18px; color: #1f2937; line-height: 1.7;")
        root.addWidget(self.weekly_questions)

        recent_title = QLabel("Recent thoughts")
        recent_title.setStyleSheet("font-size: 42px; font-weight: 700; letter-spacing: -1.1px;")
        root.addWidget(recent_title)

        refresh_button = QPushButton("Refresh")
        refresh_button.setFixedWidth(120)
        refresh_button.clicked.connect(self.refresh_notes)
        root.addWidget(refresh_button, 0, Qt.AlignmentFlag.AlignLeft)

        self.notes_list = QListWidget()
        self.notes_list.setAlternatingRowColors(False)
        root.addWidget(self.notes_list, 1)

        self.refresh_notes()
        self.load_weekly_summary()

    def _show_error(self, message: str) -> None:
        QMessageBox.critical(self, "Lume Error", message)

    def save_note(self) -> None:
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        tags_text = self.tags_input.text().strip()

        if not content:
            QMessageBox.warning(self, "Missing content", "Please write a thought before saving.")
            return

        payload = {
            "user_id": USER_ID,
            "title": title or None,
            "content": content,
            "source": "desktop",
            "category": "reflection",
            "mood": "neutral",
            "importance": 0.7,
            "tags": [tag.strip() for tag in tags_text.split(",") if tag.strip()],
        }

        try:
            response = httpx.post(f"{API_BASE_URL}/notes", json=payload, timeout=10.0)
            response.raise_for_status()
        except Exception as exc:
            self._show_error(f"Failed to save note: {exc}")
            return

        self.title_input.clear()
        self.content_input.clear()
        self.tags_input.clear()
        self.refresh_notes()

    def _note_text(self, item: dict[str, Any]) -> str:
        title = item.get("title") or "Untitled thought"
        content = item.get("content") or ""
        tags = item.get("tags") or []
        tag_line = "" if not tags else "  " + " ".join(f"#{tag}" for tag in tags)
        return f"{title}\n{content}{tag_line}"

    def refresh_notes(self) -> None:
        try:
            response = httpx.get(f"{API_BASE_URL}/notes", params={"user_id": USER_ID}, timeout=10.0)
            response.raise_for_status()
            notes = response.json()
        except Exception as exc:
            self._show_error(f"Failed to load notes: {exc}")
            self.notes_list.clear()
            self.notes_list.addItem("No notes available.")
            return

        self.notes_list.clear()
        if not notes:
            self.notes_list.addItem("No notes yet.")
            return

        for item in notes:
            label = self._note_text(item)
            list_item = QListWidgetItem(label)
            list_item.setToolTip(item.get("content") or "")
            self.notes_list.addItem(list_item)

    def load_weekly_summary(self) -> None:
        try:
            response = httpx.get(f"{API_BASE_URL}/insights/weekly", params={"user_id": USER_ID}, timeout=10.0)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            self.weekly_summary.setText("This is a placeholder for weekly reflection summaries.")
            self.weekly_tags.setText("#growthworkflow")
            self.weekly_questions.setText("• What am I repeatedly thinking about?\n• Which of these questions deserve more attention?")
            return

        self.weekly_summary.setText(data.get("summary") or "This is a placeholder for weekly reflection summaries.")
        themes = data.get("themes") or []
        self.weekly_tags.setText(" ".join(f"#{theme}" for theme in themes))
        questions = data.get("questions") or []
        self.weekly_questions.setText("\n".join(f"• {q}" for q in questions))


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Lume")
    window = LumeWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
