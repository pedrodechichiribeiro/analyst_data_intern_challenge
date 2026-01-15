# Hi, my name is Pedro.
# I'm—as of writing this—a Computer Engineering student at UFU ("Universidade Federal de Uberlândia"), from Brazil.
# This is my solution for the "System & Data Intern Take Home" challenge from GlobalVision.
# In an attempt to go beyond what was asked, I've implemented an AI-powered analysis tool, 
# utilizing SQL and Python as a base for data analysis and processing, dynamically interpreting 
# the graphs and charts for real-time analysis.
# Regardless of whether this solution will make the cut for the internship or not, I have to say 
# this experience was rather fun!
# If you are reading this, I sincerely hope you enjoy the app. Any feedback is appreciated.

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Logic modules from your files
from data_manager import DataManager
from graphs import GraphLibrary
from ai_analyst import AIAnalyst
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Set global appearance to Dark and Modern
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AnalyticsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Enterprise AI Analytics Portal")
        self.geometry("1600x900")
        
        # Initialize Logic Modules
        self.db_manager = DataManager()
        self.db_manager.load_data()
        self.graph_lib = GraphLibrary(self.db_manager)
        self.ai_analyst = AIAnalyst()

        self.current_system_prompt = ""
        self.current_data_context = ""
        
        # Graph Description Mapping
        self.descriptions = {
            "Top Products": "Identifies the highest volume products in the support queue to pinpoint systematic hardware or software failures.",
            "Severity Stack": "Breaks down the priority level of tickets per product to distinguish between high-volume noise and critical blockers.",
            "Case Types": "A categorical distribution showing whether customers are mostly reporting bugs, seeking training, or asking questions.",
            "Global Hotspots": "Geographic analysis of support load to identify regional outages or the need for localized support teams.",
            "Ticket Density": "Measures customer 'neediness' by calculating the average number of tickets generated per unique account in a region.",
            "Industry Struggles": "Segments support issues by client market sector to identify industry-specific compliance or feature gaps.",
            "Volume Trend": "A temporal view of incoming work, identifying if the support load is scaling up or stabilizing over time.",
            "Resolution Time": "Measures team efficiency and identifies 'stale' outliers that exceed the standard 5-day closing window.",
            "Backlog Growth": "Compares incoming vs. resolved cases; diverging lines indicate a growing crisis and a need for more resources."
        }

        # --- UI Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. NAVBAR
        self.nav_frame = ctk.CTkFrame(self, height=80, fg_color="#1a1c1e", corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="ew")
        
        self.button_container = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        self.button_container.pack(expand=True)
        self.setup_nav_buttons()

        # 2. MAIN CONTENT AREA
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10) # Reduced padding
        
        # --- OPTIMIZED WEIGHTS (3:1 Ratio) ---
        # 75% Graph (Column 0), 25% Sidebar (Column 1)
        # This makes the graph much bigger and the sidebar slimmer
        self.content_frame.grid_columnconfigure(0, weight=3) 
        self.content_frame.grid_columnconfigure(1, weight=1) 
        self.content_frame.grid_rowconfigure(0, weight=1)

        # LEFT SIDE: GRAPH CONTAINER
        self.graph_container = ctk.CTkFrame(self.content_frame, fg_color="#24282c")
        self.graph_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.graph_label = ctk.CTkLabel(self.graph_container, text="Data Visualization", font=("Inter", 20, "bold"))
        self.graph_label.pack(pady=(10, 5))

        # Reduced padding inside the container to maximize graph area
        self.canvas_frame = ctk.CTkFrame(self.graph_container, fg_color="#ffffff", corner_radius=8)
        self.canvas_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # RIGHT SIDE: SIDEBAR
        self.side_panel = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.side_panel.grid(row=0, column=1, sticky="nsew") 
        
        # A. Graph Summary Section
        self.info_container = ctk.CTkFrame(self.side_panel, fg_color="#24282c")
        self.info_container.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(self.info_container, text="Report Overview", font=("Inter", 16, "bold"), text_color="#3498db").pack(pady=(10, 5), padx=15, anchor="w")
        self.info_text = ctk.CTkLabel(self.info_container, text="Select a report...", font=("Inter", 13), wraplength=350, justify="left")
        self.info_text.pack(pady=(0, 15), padx=15, anchor="w")

        # B. AI Insights Section
        self.ai_container = ctk.CTkFrame(self.side_panel, fg_color="#24282c")
        self.ai_container.pack(expand=True, fill="both")
        
        ctk.CTkLabel(self.ai_container, text="AI Analyst Insights", font=("Inter", 16, "bold"), text_color="#16a085").pack(pady=10, padx=15, anchor="w")
        
        # Expand=True fills the vertical space
        self.ai_textbox = ctk.CTkTextbox(
            self.ai_container, 
            font=("Inter", 14), 
            wrap="word", 
            border_width=1, 
            border_color="#3e444c"
        )
        self.ai_textbox.pack(expand=True, fill="both", padx=15, pady=10)
        
        self.ai_button = ctk.CTkButton(
            self.ai_container, 
            text="Generate Deep Analysis", 
            command=self.run_ai_analysis,
            fg_color="#2c3e50",
            hover_color="#34495e",
            height=45,
            font=("Inter", 14, "bold")
        )
        self.ai_button.pack(pady=(5, 10), padx=15, fill="x")

        # Disclaimer
        disclaimer_text = (
            "NOTE: The data_context and system_instructions changes according with the data selected for analysis, "
            "i.e. different data will change so the generated texts maintains a minimum logic. A bigger data_context, "
            "AI model and further fine tuning will produce exponentially better results and through analysis.\n\n"
            "NOTE 2: Gemma 3 is unstable at best, so it's conclusions need human supervision and usually be re-generated multiple times. "
            "Personally, I'd use a heavier model adjusting for the machine that is running the program "
            "(in my case something like Mistral Neo, with 12B parameters). With proper hardware it could take way more data "
            "and make long term, precise, reports over time. Alas, this is just a proof of concept/demonstration meant to run "
            "on any marginally modern machine (~i5-8400 and 8-16gb RAM), so the model is rather small and may take some loading time."
        )

        self.disclaimer_label = ctk.CTkLabel(
            self.ai_container,
            text=disclaimer_text,
            font=("Inter", 11),
            text_color="#95a5a6",
            justify="left",
            anchor="w"
        )
        self.disclaimer_label.pack(side="bottom", pady=(0, 15), padx=15, fill="x")

        # BIND RESIZE EVENT
        self.ai_container.bind("<Configure>", self.adjust_disclaimer_wrap)

    def adjust_disclaimer_wrap(self, event):
        """Dynamically updates the text wrap limit based on container width."""
        new_wrap_length = event.width - 40
        if new_wrap_length > 100:
            self.disclaimer_label.configure(wraplength=new_wrap_length)

    def setup_nav_buttons(self):
        reports = [
            ("Top Products", self.graph_lib.plot_top_products),
            ("Severity Stack", self.graph_lib.plot_severity_stack),
            ("Case Types", self.graph_lib.plot_case_types),
            ("Global Hotspots", self.graph_lib.plot_global_hotspots),
            ("Ticket Density", self.graph_lib.plot_ticket_density),
            ("Industry Struggles", self.graph_lib.plot_industry_struggles),
            ("Volume Trend", self.graph_lib.plot_volume_over_time),
            ("Resolution Time", self.graph_lib.plot_resolution_time),
            ("Backlog Growth", self.graph_lib.plot_backlog_growth),
        ]

        for i, (name, func) in enumerate(reports):
            btn = ctk.CTkButton(
                self.button_container, 
                text=name, 
                command=lambda f=func, n=name: self.display_graph(f, n),
                width=130,
                height=35,
                corner_radius=6
            )
            btn.grid(row=0, column=i, padx=4, pady=10)

    def display_graph(self, plot_func, report_name):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        self.graph_label.configure(text=report_name)
        desc = self.descriptions.get(report_name, "No description available.")
        self.info_text.configure(text=desc)

        self.ai_textbox.configure(state="normal") 
        self.ai_textbox.delete("0.0", "end")
        self.ai_textbox.insert("0.0", "Ready for analysis...")
        self.ai_textbox.configure(state="disabled") 
        
        # INCREASED FIGURE SIZE: (9, 6)
        # This forces Matplotlib to generate a larger image initially, filling the larger container better.
        fig, ax = plt.subplots(figsize=(9, 6), dpi=100)
        
        self.current_system_prompt, self.current_data_context = plot_func(ax)
        
        # Tight layout minimizes white borders
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.canvas_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(expand=True, fill="both")
        plt.close(fig)
        
    def run_ai_analysis(self):
        if not self.current_data_context:
            return

        self.ai_textbox.configure(state="normal")
        self.ai_textbox.delete("0.0", "end")
        self.ai_textbox.insert("0.0", "Crunching data via Gemma 3...")
        self.update_idletasks() 

        response = self.ai_analyst.analyze(self.current_system_prompt, self.current_data_context)
        
        self.ai_textbox.delete("0.0", "end")
        self.ai_textbox.insert("0.0", response)
        self.ai_textbox.configure(state="disabled")

if __name__ == "__main__":
    app = AnalyticsApp()
    app.mainloop()