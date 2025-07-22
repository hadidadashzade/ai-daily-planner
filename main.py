import ttkbootstrap as ttk
from gui.main_ui import PlannerGUI

def main():
    root = ttk.Window()  # Instead of tk.Tk()
    app = PlannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
