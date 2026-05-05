import customtkinter as ctk
import time
import threading
from datetime import datetime

# --- الإعدادات العامة للتصميم ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") # سيتم تخصيص الألوان يدويًا

COLORS = {
    "bg": "#0B0C10",
    "card": "#1F2833",
    "accent": "#66FCF1",
    "dim": "#45A29E",
    "text": "#C5C6C7",
    "purple": "#A855F7",
    "green": "#10B981"
}

class SecureTransferApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Secure File Transfer - Python Console v4.0")
        self.geometry("1200x800")
        self.configure(fg_color=COLORS["bg"])

        self.workflow_step = 0
        self.logs = []
        self.is_processing = False

        # Grid Configuration
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_header()
        self.create_top_stats()
        self.create_main_content()
        self.create_footer()

        self.add_log("System initialized - Python Desktop Node")
        self.add_log("Awaiting handshake protocol...")

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, padx=30, pady=(30, 10), sticky="ew")

        # Title Section
        title_label = ctk.CTkLabel(header_frame, text="SECURE CONSOLE", font=("Inter", 24, "bold"), text_color="white")
        title_label.pack(side="left")

        version_badge = ctk.CTkLabel(header_frame, text="v4.0", font=("JetBrains Mono", 10, "bold"),
                                     fg_color=COLORS["card"], text_color=COLORS["accent"], corner_radius=5)
        version_badge.pack(side="left", padx=10)

        # Status Badge
        # Note: Avoided alpha channel in hex codes as it may cause issues in some Tkinter versions.
        self.status_badge = ctk.CTkLabel(header_frame, text="● CHANNEL SECURE", font=("Inter", 11, "bold"),
                                         text_color=COLORS["green"], fg_color="#142B28", corner_radius=15, padx=15)
        self.status_badge.pack(side="right")

    def create_top_stats(self):
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.grid(row=1, column=0, columnspan=2, padx=30, pady=10, sticky="ew")
        stats_frame.grid_columnconfigure((0,1,2), weight=1)

        self.token_card = self.draw_stat_card(stats_frame, "IDENTITY TOKEN", "WAIT_PK", 0)
        self.buffer_card = self.draw_stat_card(stats_frame, "OBJECT BUFFER", "Awaiting Data...", 1)
        self.tunnel_card = self.draw_stat_card(stats_frame, "TUNNEL STATUS", "PHASE 00", 2, COLORS["green"])

    def draw_stat_card(self, parent, title, value, col, val_color="white"):
        card = ctk.CTkFrame(parent, fg_color=COLORS["card"], border_color=COLORS["dim"], border_width=1, corner_radius=12)
        card.grid(row=0, column=col, padx=10, sticky="ew")

        t_label = ctk.CTkLabel(card, text=title, font=("Inter", 10, "bold"), text_color=COLORS["dim"])
        t_label.pack(pady=(15, 0), padx=20, anchor="w")

        v_label = ctk.CTkLabel(card, text=value, font=("Inter", 18, "bold"), text_color=val_color)
        v_label.pack(pady=(0, 15), padx=20, anchor="w")
        return v_label

    def create_main_content(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=2, column=0, columnspan=2, padx=30, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=1)

        # Left Column: Workflows
        workflow_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        workflow_container.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        workflow_container.grid_columnconfigure((0, 1), weight=1)

        # 1. Sender Node
        sender_node = ctk.CTkFrame(workflow_container, fg_color=COLORS["card"], corner_radius=15, border_width=1, border_color="#2D3B4C")
        sender_node.grid(row=0, column=0, sticky="nsew", padx=10)

        ctk.CTkLabel(sender_node, text="SENDER WORKFLOW", font=("Inter", 14, "bold"), text_color="white").pack(pady=(20, 5), padx=20, anchor="w")
        ctk.CTkLabel(sender_node, text="Secure Transmission Node", font=("Inter", 10), text_color=COLORS["dim"]).pack(padx=20, anchor="w")

        self.sender_btns = []
        steps = [
            (1, "Receive Public Key"),
            (3, "Select File"),
            (5, "Generate Session Key"),
            (7, "Encrypt & Send File")
        ]

        for s, label in steps:
            btn = ctk.CTkButton(sender_node, text=f"0{s} {label}",
                               font=("Inter", 12, "bold"),
                               fg_color="transparent", border_width=1, border_color="#215250",
                               hover_color="#142B28", text_color="white",
                               height=40, anchor="w",
                               command=lambda s=s, l=label: self.run_step(s, l))
            btn.pack(pady=5, padx=20, fill="x")
            self.sender_btns.append(btn)

        # 2. Receiver Node
        receiver_node = ctk.CTkFrame(workflow_container, fg_color=COLORS["card"], corner_radius=15, border_width=1, border_color="#2D3B4C")
        receiver_node.grid(row=0, column=1, sticky="nsew", padx=10)

        ctk.CTkLabel(receiver_node, text="RECEIVER WORKFLOW", font=("Inter", 14, "bold"), text_color="white").pack(pady=(20, 5), padx=20, anchor="w")
        ctk.CTkLabel(receiver_node, text="Target Capture Node", font=("Inter", 10), text_color=COLORS["dim"]).pack(padx=20, anchor="w")

        r_steps = [
            (2, "Generate Keys"),
            (4, "Decrypt Session Key"),
            (6, "Decrypt & Save File")
        ]

        for s, label in r_steps:
            btn = ctk.CTkButton(receiver_node, text=f"0{s} {label}",
                               font=("Inter", 12, "bold"),
                               fg_color="transparent", border_width=1, border_color="#361E50",
                               hover_color="#241435", text_color=COLORS["purple"],
                               height=40, anchor="w",
                               command=lambda s=s, l=label: self.run_step(s, l))
            btn.pack(pady=5, padx=20, fill="x")

        # Progress Bar Area
        progress_frame = ctk.CTkFrame(receiver_node, fg_color="#0B0C10", corner_radius=10)
        progress_frame.pack(pady=20, padx=20, fill="x", side="bottom")
        self.prog_label = ctk.CTkLabel(progress_frame, text="LINK PROGRESS: 0%", font=("JetBrains Mono", 10), text_color=COLORS["accent"])
        self.prog_label.pack(pady=(10, 5))
        self.progress_bar = ctk.CTkProgressBar(progress_frame, progress_color=COLORS["accent"], fg_color="#1F2833")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(0, 15), padx=20, fill="x")

        # Right Column: Logs
        log_node = ctk.CTkFrame(main_frame, fg_color=COLORS["card"], corner_radius=15, border_width=1, border_color="#2D3B4C")
        log_node.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(log_node, text="AUDIT LOG", font=("Inter", 12, "bold"), text_color="white").pack(pady=15, padx=20, anchor="w")

        self.log_box = ctk.CTkTextbox(log_node, fg_color="transparent", font=("JetBrains Mono", 11), text_color=COLORS["dim"])
        self.log_box.pack(expand=True, fill="both", padx=10, pady=10)

    def create_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent", height=50)
        footer.grid(row=3, column=0, columnspan=2, padx=30, pady=20, sticky="ew")

        ctk.CTkLabel(footer, text="CRYPT_ID: 0x82A1", font=("JetBrains Mono", 9, "bold"), text_color="#C5C6C7").pack(side="left")
        ctk.CTkLabel(footer, text="SESSION_ACTIVE", font=("JetBrains Mono", 9, "bold"), text_color=COLORS["green"]).pack(side="right")

    def add_log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] :: {msg}\n"
        self.log_box.insert("0.0", log_entry)

    def run_step(self, step_num, label):
        if self.is_processing: return

        # Simple step validation (must be sequential)
        if step_num != self.workflow_step + 1:
            self.add_log(f"ERROR: Protocol violation. Expected Step 0{self.workflow_step + 1}")
            return

        self.is_processing = True
        self.add_log(f"INIT: {label}...")

        def processing_thread():
            time.sleep(1.2) # Simulate crypto work
            self.workflow_step = step_num
            self.after(0, self.update_ui_after_step, label)

        threading.Thread(target=processing_thread).start()

    def update_ui_after_step(self, label):
        self.is_processing = False
        self.add_log(f"SUCCESS: {label} verified")

        # Update progress
        progress_val = self.workflow_step / 7
        self.progress_bar.set(progress_val)
        self.prog_label.configure(text=f"LINK PROGRESS: {int(progress_val*100)}%")

        # Update top cards
        self.tunnel_card.configure(text=f"PHASE 0{self.workflow_step}")
        if self.workflow_step >= 1: self.token_card.configure(text="AUTH_VERIFIED")
        if self.workflow_step >= 3: self.buffer_card.configure(text="SECURE_V4.PKG")

        if self.workflow_step == 7:
            self.add_log("PROTOCOL COMPLETE. TUNNEL STATIC.")

if __name__ == "__main__":
    app = SecureTransferApp()
    app.mainloop()
