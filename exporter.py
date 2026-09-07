"""
Excel Export module for Laboratorio Gerenciador
Handles export of all data to Excel files
"""

import pandas as pd
import os
from datetime import datetime
from database import get_all_records, get_table_columns


def export_to_excel(output_path=None):
    """Export all data to a single Excel file with multiple sheets"""
    if output_path is None:
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f'relatorio_laboratorio_{timestamp}.xlsx'
        )
    
    # Define tables and their display names
    tables = {
        'incidentes_colaboradores': 'Incidentes - Colaboradores',
        'incidentes_amostra': 'Incidentes - Amostra',
        'temperaturas': 'Temperaturas',
        'manutencao_equipamentos': 'Manutenção dos Equipamentos',
        'gerenciamento_riscos': 'Gerenciamento de Riscos',
        'troca_almotolias': 'Troca de Almotolias',
        'analise_pendencias': 'Análise de Pendências'
    }
    
    # Create Excel writer
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for table_name, sheet_name in tables.items():
            # Get data from database
            records = get_all_records(table_name)
            
            if records:
                # Convert to DataFrame
                columns = get_table_columns(table_name)
                df = pd.DataFrame([dict(zip(columns, record)) for record in records])
                
                # Format datetime columns
                for col in df.columns:
                    if 'data' in col.lower() or 'hora' in col.lower():
                        try:
                            df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d %H:%M:%S')
                        except:
                            pass
                
                # Write to Excel
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Auto-adjust column widths
                worksheet = writer.sheets[sheet_name]
                for idx, col in enumerate(df.columns):
                    # Set column width based on content
                    max_len = max(
                        df[col].astype(str).map(len).max(),
                        len(col)
                    ) + 2
                    worksheet.column_dimensions[chr(65 + idx)].width = min(max_len, 50)
    
    return output_path


def export_single_table_to_excel(table_name, output_path=None):
    """Export a single table to Excel"""
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sheet_name = table_name.replace('_', ' ').title()
        output_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f'{sheet_name}_{timestamp}.xlsx'
        )
    
    # Get data
    records = get_all_records(table_name)
    
    if records:
        columns = get_table_columns(table_name)
        df = pd.DataFrame([dict(zip(columns, record)) for record in records])
        
        # Format datetime columns
        for col in df.columns:
            if 'data' in col.lower() or 'hora' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pass
        
        # Write to Excel
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=table_name.replace('_', ' ').title(), index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets[table_name.replace('_', ' ').title()]
            for idx, col in enumerate(df.columns):
                max_len = max(
                    df[col].astype(str).map(len).max(),
                    len(col)
                ) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_len, 50)
    
    return output_path


if __name__ == '__main__':
    # Test export
    output = export_to_excel()
    print(f"Export successful: {output}")
