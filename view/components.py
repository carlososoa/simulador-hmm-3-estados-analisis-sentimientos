import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (60, 60, 80)
BLUE = (66, 133, 244)
LIGHT_BLUE = (100, 160, 255)
CELL_BG = (240, 240, 245)
CELL_BORDER = (180, 180, 180)
CELL_ACTIVE = (100, 149, 237)

FPS = 30


class Button:
    def __init__(self, rect, text, font, color, hover_color, text_color=WHITE, callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.callback = callback
        self.hovered = False
        self.visible = True

    def draw(self, screen):
        if not self.visible:
            return
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        pygame.draw.rect(screen, (100, 100, 140), self.rect, 2, border_radius=6)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if not self.visible:
            return False
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and self.callback:
                self.callback()
                return True
        return False


class InputCell:
    def __init__(self, rect, value, font):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.value = ""
        self.text = ""
        self.set_value(value)
        self.active = False

    def set_value(self, value):
        self.value = str(value)
        self.text = self.value

    def get_float(self):
        try:
            return float(self.text)
        except ValueError:
            return 0.0

    def draw(self, screen):
        color = CELL_ACTIVE if self.active else CELL_BORDER
        pygame.draw.rect(screen, CELL_BG, self.rect, border_radius=3)
        pygame.draw.rect(screen, color, self.rect, 2, border_radius=3)
        display_text = self.text
        text_surf = self.font.render(display_text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            was_active = self.active
            self.active = self.rect.collidepoint(event.pos)
            if self.active and not was_active:
                self.text = ""
            return self.active
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.active = False
                try:
                    v = float(self.text)
                    self.text = f"{v:.3g}"
                    self.value = self.text
                except ValueError:
                    self.text = self.value
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.text = self.value
                self.active = False
            else:
                char = event.unicode
                if char in '0123456789.':
                    if char == '.' and '.' in self.text:
                        pass
                    else:
                        self.text += char
            return True
        return False


class MatrixGrid:
    def __init__(self, x, y, title, rows, cols, values, row_labels, col_labels, font):
        self.x = x
        self.y = y
        self.title = title
        self.rows = rows
        self.cols = cols
        self.cell_w = 70
        self.cell_h = 32
        self.gap = 4
        self.font = font
        self.title_font = pygame.font.Font(None, 22)
        self.row_labels = row_labels
        self.col_labels = col_labels

        self.cells = []
        for r in range(rows):
            row_cells = []
            for c in range(cols):
                cx = x + 70 + c * (self.cell_w + self.gap)
                cy = y + 35 + r * (self.cell_h + self.gap)
                cell = InputCell((cx, cy, self.cell_w, self.cell_h), values[r][c], font)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def draw(self, screen):
        title_surf = self.title_font.render(self.title, True, WHITE)
        screen.blit(title_surf, (self.x, self.y - 5))

        for c, label in enumerate(self.col_labels):
            cx = self.x + 70 + c * (self.cell_w + self.gap) + self.cell_w // 2
            surf = self.font.render(label, True, WHITE)
            screen.blit(surf, (cx - surf.get_width() // 2, self.y + 8))

        for r in range(self.rows):
            surf = self.font.render(self.row_labels[r], True, WHITE)
            y_pos = self.y + 35 + r * (self.cell_h + self.gap) + self.cell_h // 2
            screen.blit(surf, (self.x + 5, y_pos - surf.get_height() // 2))

            for c in range(self.cols):
                self.cells[r][c].draw(screen)

    def handle_event(self, event):
        for row in self.cells:
            for cell in row:
                cell.handle_event(event)

    def get_values(self):
        return [[cell.get_float() for cell in row] for row in self.cells]

    def deactivate_all(self):
        for row in self.cells:
            for cell in row:
                cell.active = False
