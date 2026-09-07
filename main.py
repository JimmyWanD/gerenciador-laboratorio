"""
Laboratorio Gerenciador - Main Application
A complete management system for clinical laboratory
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
from datetime import datetime
from database import (
    initialize_database, get_all_records, insert_record, 
    update_record, delete_record, search_records, get_table_columns
)
from exporter import export_to_excel


class LaboratorioApp:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Laboratório")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configure styles
        self.configure_styles()
        
        # Initialize database
        initialize_database()
        
        # Create main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create menu bar
        self.create_menu()
        
        # Create category buttons
        self.create_category_buttons()
        
        # Current active form
        self.current_form = None
        self.current_table = None
        
        # Data for current view
        self.current_data = []
        
        # Setup main content area
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Show welcome message
        self.show_welcome()
    
    def configure_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        
        # Configure main styles
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('TEntry', font=('Arial', 10))
        style.configure('TCombobox', font=('Arial', 10))
        
        # Treeview styles
        style.configure('Treeview', font=('Arial', 10), rowheight=25)
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        
        # Header style
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'), background='#f0f0f0')
        
        # Button styles
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'), foreground='white', background='#0078d7')
        style.configure('Success.TButton', font=('Arial', 10, 'bold'), foreground='white', background='#28a745')
        style.configure('Danger.TButton', font=('Arial', 10, 'bold'), foreground='white', background='#dc3545')
        style.configure('Warning.TButton', font=('Arial', 10, 'bold'), foreground='black', background='#ffc107')
        
        # Set theme
        try:
            style.theme_use('clam')
        except:
            pass
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exportar para Excel", command=self.export_all_to_excel)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Atualizar", command=self.refresh_current_view)
        menubar.add_cascade(label="Visualizar", menu=view_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Sobre", command=self.show_about)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_category_buttons(self):
        """Create buttons for each category"""
        categories = [
            ("Incidentes (Colaboradores)", "incidentes_colaboradores"),
            ("Incidentes (Amostra)", "incidentes_amostra"),
            ("Temperaturas", "temperaturas"),
            ("Manutenção dos Equipamentos", "manutencao_equipamentos"),
            ("Gerenciamento de Riscos", "gerenciamento_riscos"),
            ("Troca de Almotolias", "troca_almotolias"),
            ("Análise de Pendências", "analise_pendencias")
        ]
        
        # Create button frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create buttons
        for i, (text, table_name) in enumerate(categories):
            btn = ttk.Button(
                button_frame, 
                text=text, 
                command=lambda t=table_name, txt=text: self.show_category_form(t, txt),
                style='Primary.TButton',
                width=25
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky=tk.W+tk.E)
    
    def show_welcome(self):
        """Show welcome message"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create welcome frame
        welcome_frame = ttk.Frame(self.content_frame)
        welcome_frame.pack(fill=tk.BOTH, expand=True)
        
        # Welcome label
        welcome_label = ttk.Label(
            welcome_frame,
            text="Bem-vindo ao Gerenciador de Laboratório",
            style='Header.TLabel'
        )
        welcome_label.pack(pady=20)
        
        # Description
        desc_label = ttk.Label(
            welcome_frame,
            text="Selecione uma categoria acima para começar a registrar dados.",
            font=('Arial', 12)
        )
        desc_label.pack(pady=10)
        
        # Features list
        features = [
            "• Incidentes com Colaboradores",
            "• Incidentes com Amostras",
            "• Registro de Temperaturas",
            "• Manutenção de Equipamentos (Controle e Calibração)",
            "• Gerenciamento de Riscos",
            "• Troca de Almotolias",
            "• Análise de Pendências",
            "• Exportação para Excel"
        ]
        
        for feature in features:
            ttk.Label(welcome_frame, text=feature, font=('Arial', 10)).pack(anchor=tk.W, padx=20, pady=2)
    
    def show_category_form(self, table_name, display_name):
        """Show form for a specific category"""
        self.current_table = table_name
        
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create main form frame
        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(form_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            header_frame, 
            text=display_name, 
            style='Header.TLabel'
        ).pack(side=tk.LEFT)
        
        # Action buttons frame
        action_frame = ttk.Frame(header_frame)
        action_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            action_frame,
            text="Adicionar",
            command=lambda: self.show_add_dialog(table_name, display_name),
            style='Success.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Atualizar",
            command=lambda: self.refresh_current_view(),
            style='Warning.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Exportar Excel",
            command=lambda: self.export_single_to_excel(table_name, display_name),
            style='Primary.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(form_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Pesquisar:").pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_entry.bind('<KeyRelease>', lambda e: self.search_data(table_name))
        
        # Treeview frame
        tree_frame = ttk.Frame(form_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview
        self.create_treeview(tree_frame, table_name)
        
        # Edit/Delete buttons
        edit_delete_frame = ttk.Frame(form_frame)
        edit_delete_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(
            edit_delete_frame,
            text="Editar Selecionado",
            command=lambda: self.edit_selected_record(table_name, display_name),
            style='Warning.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            edit_delete_frame,
            text="Excluir Selecionado",
            command=lambda: self.delete_selected_record(table_name),
            style='Danger.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Load data
        self.load_data_to_treeview(table_name)
    
    def create_treeview(self, parent_frame, table_name):
        """Create Treeview for displaying data"""
        # Get column names
        columns = get_table_columns(table_name)
        
        # Create Treeview
        self.tree = ttk.Treeview(parent_frame, columns=columns, show='headings', selectmode='browse')
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col.replace('_', ' ').title())
            self.tree.column(col, width=150, anchor=tk.W)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click to edit
        display_names = {
            "incidentes_colaboradores": "Incidentes (Colaboradores)",
            "incidentes_amostra": "Incidentes (Amostra)",
            "temperaturas": "Temperaturas",
            "manutencao_equipamentos": "Manutenção dos Equipamentos",
            "gerenciamento_riscos": "Gerenciamento de Riscos",
            "troca_almotolias": "Troca de Almotolias",
            "analise_pendencias": "Análise de Pendências"
        }
        self.tree.bind('<Double-1>', lambda e: self.edit_selected_record(table_name, display_names.get(table_name, "")))
    
    def load_data_to_treeview(self, table_name):
        """Load data from database to Treeview"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get data
        records = get_all_records(table_name)
        self.current_data = records
        
        # Insert data into Treeview
        columns = get_table_columns(table_name)
        for record in records:
            values = [record[col] for col in columns]
            self.tree.insert('', tk.END, values=values, iid=record['id'])
    
    def search_data(self, table_name):
        """Search data in the current table"""
        search_term = self.search_var.get()
        
        if not search_term:
            self.load_data_to_treeview(table_name)
            return
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Search data
        records = search_records(table_name, search_term)
        self.current_data = records
        
        # Insert results
        columns = get_table_columns(table_name)
        for record in records:
            values = [record[col] for col in columns]
            self.tree.insert('', tk.END, values=values, iid=record['id'])
    
    def refresh_current_view(self):
        """Refresh the current view"""
        if self.current_table:
            self.load_data_to_treeview(self.current_table)
            self.search_var.set('')
    
    def show_add_dialog(self, table_name, display_name):
        """Show dialog for adding a new record"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Adicionar {display_name}")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create form
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Get columns for this table
        columns = get_table_columns(table_name)
        self.form_fields = {}
        
        # Skip 'id' columns
        skip_columns = ['id']
        if table_name == 'manutencao_equipamentos':
            skip_columns.extend(['data_manutencao', 'proxima_manutencao'])
        elif table_name == 'troca_almotolias':
            skip_columns.extend(['data_troca', 'proxima_troca'])
        elif table_name == 'gerenciamento_riscos':
            skip_columns.append('data_identificacao')
        elif table_name == 'analise_pendencias':
            skip_columns.append('data_criacao')
        elif table_name == 'temperaturas':
            skip_columns.append('data_hora')
        
        for i, col in enumerate(columns):
            if col in skip_columns:
                continue
            
            # Create label
            label_text = col.replace('_', ' ').title()
            ttk.Label(form_frame, text=label_text + ":").grid(row=i, column=0, sticky=tk.W, pady=5)
            
            # Create input field based on column type
            if col == 'data_hora' and table_name == 'incidentes_colaboradores':
                # Date/time field for incidentes_colaboradores - allow user input
                entry = ttk.Entry(form_frame, width=30)
                entry.insert(0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                entry.grid(row=i, column=1, sticky=tk.W, pady=5)
                self.form_fields[col] = entry
            elif 'data' in col.lower() or 'hora' in col.lower():
                # Date/time field with auto timestamp
                entry = ttk.Entry(form_frame, width=30)
                entry.insert(0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                entry.grid(row=i, column=1, sticky=tk.W, pady=5)
                self.form_fields[col] = entry
            elif col in ['tipo', 'nivel', 'prioridade', 'status']:
                # Dropdown field
                options = []
                if col == 'tipo' and table_name == 'manutencao_equipamentos':
                    options = ['Controle', 'Calibração']
                elif col == 'nivel':
                    options = ['Baixo', 'Médio', 'Alto']
                elif col == 'prioridade':
                    options = ['Baixa', 'Média', 'Alta']
                elif col == 'status':
                    options = ['Pendente', 'Concluído', 'Em Andamento']
                
                if options:
                    combo = ttk.Combobox(form_frame, values=options, width=27, state='readonly')
                    combo.grid(row=i, column=1, sticky=tk.W, pady=5)
                    self.form_fields[col] = combo
                else:
                    entry = ttk.Entry(form_frame, width=30)
                    entry.grid(row=i, column=1, sticky=tk.W, pady=5)
                    self.form_fields[col] = entry
            else:
                # Regular text field
                entry = ttk.Entry(form_frame, width=30)
                entry.grid(row=i, column=1, sticky=tk.W, pady=5)
                self.form_fields[col] = entry
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(columns), column=0, columnspan=2, pady=20)
        
        ttk.Button(
            button_frame,
            text="Salvar",
            command=lambda: self.save_record(dialog, table_name),
            style='Success.TButton'
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=dialog.destroy,
            style='Danger.TButton'
        ).pack(side=tk.LEFT, padx=10)
    
    def save_record(self, dialog, table_name):
        """Save a new record to the database"""
        # Collect data from form
        data = {}
        for col, widget in self.form_fields.items():
            value = widget.get()
            if isinstance(widget, ttk.Combobox):
                value = widget.get()
            
            # Convert empty strings to None for numeric fields
            if col in ['temperatura']:
                if value == '':
                    value = None
                else:
                    try:
                        value = float(value)
                    except:
                        messagebox.showerror("Erro", f"Valor inválido para {col}")
                        return
            
            data[col] = value
        
        # Add timestamp for specific columns
        if table_name == 'incidentes_colaboradores':
            if 'data_hora' not in data or not data['data_hora']:
                data['data_hora'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elif table_name == 'incidentes_amostra':
            if 'data_hora' not in data or not data['data_hora']:
                data['data_hora'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elif table_name == 'temperaturas':
            if 'data_hora' not in data or not data['data_hora']:
                data['data_hora'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elif table_name == 'manutencao_equipamentos':
            if 'data_manutencao' not in data or not data['data_manutencao']:
                data['data_manutencao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elif table_name == 'gerenciamento_riscos':
            if 'data_identificacao' not in data or not data['data_identificacao']:
                data['data_identificacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elif table_name == 'analise_pendencias':
            if 'data_criacao' not in data or not data['data_criacao']:
                data['data_criacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Insert into database
        try:
            insert_record(table_name, data)
            messagebox.showinfo("Sucesso", "Registro adicionado com sucesso!")
            dialog.destroy()
            self.refresh_current_view()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar registro: {str(e)}")
    
    def edit_selected_record(self, table_name, display_name):
        """Edit the selected record"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um registro para editar")
            return
        
        record_id = selected[0]
        
        # Get the record data
        records = get_all_records(table_name)
        record = next((r for r in records if str(r['id']) == record_id), None)
        
        if not record:
            messagebox.showerror("Erro", "Registro não encontrado")
            return
        
        # Show edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Editar {display_name}")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create form
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Get columns for this table
        columns = get_table_columns(table_name)
        self.edit_form_fields = {}
        self.edit_record_id = record_id
        
        for i, col in enumerate(columns):
            if col == 'id':
                continue
            
            # Create label
            label_text = col.replace('_', ' ').title()
            ttk.Label(form_frame, text=label_text + ":").grid(row=i, column=0, sticky=tk.W, pady=5)
            
            # Create input field
            if 'data' in col.lower() or 'hora' in col.lower():
                entry = ttk.Entry(form_frame, width=30)
                # For incidentes_colaboradores, allow empty data_hora
                if col == 'data_hora' and table_name == 'incidentes_colaboradores':
                    entry.insert(0, str(record[col]) if record[col] else '')
                else:
                    entry.insert(0, str(record[col]) if record[col] else datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                entry.grid(row=i, column=1, sticky=tk.W, pady=5)
                self.edit_form_fields[col] = entry
            elif col in ['tipo', 'nivel', 'prioridade', 'status']:
                options = []
                if col == 'tipo' and table_name == 'manutencao_equipamentos':
                    options = ['Controle', 'Calibração']
                elif col == 'nivel':
                    options = ['Baixo', 'Médio', 'Alto']
                elif col == 'prioridade':
                    options = ['Baixa', 'Média', 'Alta']
                elif col == 'status':
                    options = ['Pendente', 'Concluído', 'Em Andamento']
                
                if options:
                    combo = ttk.Combobox(form_frame, values=options, width=27, state='readonly')
                    combo.set(str(record[col]) if record[col] else options[0])
                    combo.grid(row=i, column=1, sticky=tk.W, pady=5)
                    self.edit_form_fields[col] = combo
                else:
                    entry = ttk.Entry(form_frame, width=30)
                    entry.insert(0, str(record[col]) if record[col] else '')
                    entry.grid(row=i, column=1, sticky=tk.W, pady=5)
                    self.edit_form_fields[col] = entry
            else:
                entry = ttk.Entry(form_frame, width=30)
                entry.insert(0, str(record[col]) if record[col] else '')
                entry.grid(row=i, column=1, sticky=tk.W, pady=5)
                self.edit_form_fields[col] = entry
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(columns), column=0, columnspan=2, pady=20)
        
        ttk.Button(
            button_frame,
            text="Salvar",
            command=lambda: self.update_record_data(dialog, table_name),
            style='Success.TButton'
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=dialog.destroy,
            style='Danger.TButton'
        ).pack(side=tk.LEFT, padx=10)
    
    def update_record_data(self, dialog, table_name):
        """Update the selected record in the database"""
        # Collect data from form
        data = {}
        for col, widget in self.edit_form_fields.items():
            value = widget.get()
            if isinstance(widget, ttk.Combobox):
                value = widget.get()
            
            # Convert empty strings to None for numeric fields
            if col in ['temperatura']:
                if value == '':
                    value = None
                else:
                    try:
                        value = float(value)
                    except:
                        messagebox.showerror("Erro", f"Valor inválido para {col}")
                        return
            
            data[col] = value
        
        # Update in database
        try:
            update_record(table_name, self.edit_record_id, data)
            messagebox.showinfo("Sucesso", "Registro atualizado com sucesso!")
            dialog.destroy()
            self.refresh_current_view()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar registro: {str(e)}")
    
    def delete_selected_record(self, table_name):
        """Delete the selected record"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um registro para excluir")
            return
        
        record_id = selected[0]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este registro?"):
            return
        
        # Delete from database
        try:
            delete_record(table_name, record_id)
            messagebox.showinfo("Sucesso", "Registro excluído com sucesso!")
            self.refresh_current_view()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao excluir registro: {str(e)}")
    
    def export_all_to_excel(self):
        """Export all data to Excel"""
        try:
            # Ask for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension='.xlsx',
                filetypes=[('Excel files', '*.xlsx'), ('All files', '*.*')],
                title='Salvar relatório como'
            )
            
            if file_path:
                output = export_to_excel(file_path)
                messagebox.showinfo("Sucesso", f"Dados exportados para: {output}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar: {str(e)}")
    
    def export_single_to_excel(self, table_name, display_name):
        """Export single table to Excel"""
        try:
            # Ask for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension='.xlsx',
                filetypes=[('Excel files', '*.xlsx'), ('All files', '*.*')],
                title=f'Salvar {display_name} como'
            )
            
            if file_path:
                from exporter import export_single_table_to_excel
                output = export_single_table_to_excel(table_name, file_path)
                messagebox.showinfo("Sucesso", f"Dados exportados para: {output}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        Gerenciador de Laboratório
        Versão 1.0
        
        Aplicativo para gerenciamento de laboratório de análises clínicas.
        
        Funcionalidades:
        - Incidentes com Colaboradores
        - Incidentes com Amostras
        - Registro de Temperaturas
        - Manutenção de Equipamentos
        - Gerenciamento de Riscos
        - Troca de Almotolias
        - Análise de Pendências
        - Exportação para Excel
        
        Desenvolvido com Python e Tkinter
        """
        messagebox.showinfo("Sobre", about_text)


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = LaboratorioApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
