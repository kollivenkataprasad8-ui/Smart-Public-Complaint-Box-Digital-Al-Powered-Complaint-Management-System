"""
Create UI mockup screenshots for the report
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

def create_web_interface_mockup():
    """Create a mockup of the web interface"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Browser window
    browser = FancyBboxPatch((0.5, 0.5), 13, 9, boxstyle="round,pad=0.05", 
                            edgecolor='#2c3e50', facecolor='white', linewidth=3)
    ax.add_patch(browser)
    
    # Browser header
    header = Rectangle((0.5, 9), 13, 0.5, facecolor='#2c3e50')
    ax.add_patch(header)
    ax.text(7, 9.25, 'Smart Public Complaint Box - Web Portal', 
           ha='center', va='center', fontsize=14, weight='bold', color='white')
    
    # Navigation bar
    nav = Rectangle((0.5, 8.3), 13, 0.6, facecolor='#3498db')
    ax.add_patch(nav)
    nav_items = ['Home', 'Submit Complaint', 'Track Status', 'Dashboard', 'Profile']
    for i, item in enumerate(nav_items):
        ax.text(1.5 + i*2.5, 8.6, item, ha='center', va='center', 
               fontsize=11, weight='bold', color='white')
    
    # Main content area - Submit Complaint Form
    ax.text(7, 7.8, 'Submit New Complaint', ha='center', va='center', 
           fontsize=16, weight='bold', color='#2c3e50')
    
    # Form fields
    form_y = 7.2
    field_height = 0.4
    field_spacing = 0.6
    
    fields = [
        ('Title:', 'Enter complaint title'),
        ('Description:', 'Describe your issue in detail'),
        ('Location:', 'Enter location'),
        ('Category:', 'Auto-detected by AI')
    ]
    
    for i, (label, placeholder) in enumerate(fields):
        y_pos = form_y - i * field_spacing
        
        # Label
        ax.text(1.5, y_pos, label, ha='left', va='center', 
               fontsize=11, weight='bold', color='#2c3e50')
        
        # Input field
        if i == 1:  # Description field (larger)
            field = Rectangle((3, y_pos - 0.5), 9.5, 1, 
                            facecolor='#ecf0f1', edgecolor='#95a5a6', linewidth=1.5)
            ax.add_patch(field)
            ax.text(3.2, y_pos, placeholder, ha='left', va='center', 
                   fontsize=10, color='#7f8c8d', style='italic')
        else:
            field = Rectangle((3, y_pos - field_height/2), 9.5, field_height, 
                            facecolor='#ecf0f1', edgecolor='#95a5a6', linewidth=1.5)
            ax.add_patch(field)
            ax.text(3.2, y_pos, placeholder, ha='left', va='center', 
                   fontsize=10, color='#7f8c8d', style='italic')
    
    # Upload button
    upload_btn = FancyBboxPatch((1.5, 3.5), 2.5, 0.5, boxstyle="round,pad=0.05",
                               edgecolor='#95a5a6', facecolor='#ecf0f1', linewidth=1.5)
    ax.add_patch(upload_btn)
    ax.text(2.75, 3.75, '📎 Upload Photo', ha='center', va='center', 
           fontsize=10, weight='bold', color='#2c3e50')
    
    # Submit button
    submit_btn = FancyBboxPatch((5, 2.5), 4, 0.7, boxstyle="round,pad=0.05",
                               edgecolor='#27ae60', facecolor='#2ecc71', linewidth=2)
    ax.add_patch(submit_btn)
    ax.text(7, 2.85, 'Submit Complaint', ha='center', va='center', 
           fontsize=14, weight='bold', color='white')
    
    # Info box
    info_box = FancyBboxPatch((1.5, 1), 11, 1, boxstyle="round,pad=0.05",
                             edgecolor='#3498db', facecolor='#ebf5fb', linewidth=2)
    ax.add_patch(info_box)
    ax.text(7, 1.7, 'AI-Powered System', ha='center', va='center', 
           fontsize=12, weight='bold', color='#2c3e50')
    ax.text(7, 1.35, 'Your complaint will be automatically categorized and assigned to the relevant department', 
           ha='center', va='center', fontsize=9, color='#34495e')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/complaint_system/results/web_interface_mockup.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Web interface mockup saved")
    plt.close()


def create_mobile_interface_mockup():
    """Create a mockup of the mobile interface"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 10))
    
    # Mobile screen 1 - Submit Complaint
    ax1.set_xlim(0, 6)
    ax1.set_ylim(0, 12)
    ax1.axis('off')
    
    # Phone frame
    phone1 = FancyBboxPatch((0.5, 0.5), 5, 11, boxstyle="round,pad=0.1", 
                           edgecolor='#2c3e50', facecolor='white', linewidth=4)
    ax1.add_patch(phone1)
    
    # Status bar
    status = Rectangle((0.5, 11), 5, 0.5, facecolor='#2c3e50')
    ax1.add_patch(status)
    ax1.text(3, 11.25, '9:41 AM  📶 🔋', ha='center', va='center', 
            fontsize=10, color='white')
    
    # App header
    header1 = Rectangle((0.5, 10.2), 5, 0.7, facecolor='#3498db')
    ax1.add_patch(header1)
    ax1.text(3, 10.55, 'Submit Complaint', ha='center', va='center', 
            fontsize=14, weight='bold', color='white')
    
    # Form content
    ax1.text(3, 9.5, 'New Complaint', ha='center', va='center', 
            fontsize=13, weight='bold', color='#2c3e50')
    
    # Input fields
    fields_y = [8.8, 7.8, 6.8, 5.8]
    field_labels = ['Title', 'Description', 'Location', 'Upload Photo']
    
    for i, (y, label) in enumerate(zip(fields_y, field_labels)):
        field = FancyBboxPatch((1, y - 0.3), 4, 0.6, boxstyle="round,pad=0.05",
                              edgecolor='#95a5a6', facecolor='#ecf0f1', linewidth=1.5)
        ax1.add_patch(field)
        ax1.text(1.3, y, label, ha='left', va='center', 
                fontsize=10, color='#7f8c8d')
    
    # AI indicator
    ai_box = FancyBboxPatch((1, 4.5), 4, 0.8, boxstyle="round,pad=0.05",
                           edgecolor='#9b59b6', facecolor='#f4ecf7', linewidth=2)
    ax1.add_patch(ai_box)
    ax1.text(3, 5, '🤖 AI Categorization', ha='center', va='center', 
            fontsize=11, weight='bold', color='#8e44ad')
    ax1.text(3, 4.7, 'Automatic', ha='center', va='center', 
            fontsize=9, color='#8e44ad')
    
    # Submit button
    submit = FancyBboxPatch((1.5, 3.2), 3, 0.7, boxstyle="round,pad=0.05",
                          edgecolor='#27ae60', facecolor='#2ecc71', linewidth=2)
    ax1.add_patch(submit)
    ax1.text(3, 3.55, 'SUBMIT', ha='center', va='center', 
            fontsize=13, weight='bold', color='white')
    
    # Mobile screen 2 - Track Status
    ax2.set_xlim(0, 6)
    ax2.set_ylim(0, 12)
    ax2.axis('off')
    
    # Phone frame
    phone2 = FancyBboxPatch((0.5, 0.5), 5, 11, boxstyle="round,pad=0.1", 
                           edgecolor='#2c3e50', facecolor='white', linewidth=4)
    ax2.add_patch(phone2)
    
    # Status bar
    status2 = Rectangle((0.5, 11), 5, 0.5, facecolor='#2c3e50')
    ax2.add_patch(status2)
    ax2.text(3, 11.25, '9:41 AM  📶 🔋', ha='center', va='center', 
            fontsize=10, color='white')
    
    # App header
    header2 = Rectangle((0.5, 10.2), 5, 0.7, facecolor='#3498db')
    ax2.add_patch(header2)
    ax2.text(3, 10.55, 'My Complaints', ha='center', va='center', 
            fontsize=14, weight='bold', color='white')
    
    # Complaint cards
    complaints = [
        ('Water Supply Issue', 'High', 'In Progress', '#e74c3c'),
        ('Road Pothole', 'Medium', 'Submitted', '#f39c12'),
        ('Power Cut', 'Low', 'Resolved', '#2ecc71')
    ]
    
    card_y = 9.2
    for title, priority, status, color in complaints:
        # Card
        card = FancyBboxPatch((0.8, card_y - 1.2), 4.4, 1.3, boxstyle="round,pad=0.05",
                             edgecolor='#bdc3c7', facecolor='#f8f9fa', linewidth=2)
        ax2.add_patch(card)
        
        # Title
        ax2.text(1.2, card_y - 0.4, title, ha='left', va='center', 
                fontsize=11, weight='bold', color='#2c3e50')
        
        # Priority badge
        priority_badge = FancyBboxPatch((1.2, card_y - 0.75), 1.2, 0.25, 
                                       boxstyle="round,pad=0.02",
                                       edgecolor=color, facecolor=color, linewidth=1)
        ax2.add_patch(priority_badge)
        ax2.text(1.8, card_y - 0.625, priority, ha='center', va='center', 
                fontsize=8, weight='bold', color='white')
        
        # Status
        ax2.text(4.8, card_y - 0.625, status, ha='right', va='center', 
                fontsize=9, color='#7f8c8d', style='italic')
        
        # View button
        view_btn = FancyBboxPatch((3.5, card_y - 1.05), 1.2, 0.3, 
                                 boxstyle="round,pad=0.02",
                                 edgecolor='#3498db', facecolor='#3498db', linewidth=1)
        ax2.add_patch(view_btn)
        ax2.text(4.1, card_y - 0.9, 'View Details', ha='center', va='center', 
                fontsize=8, weight='bold', color='white')
        
        card_y -= 1.8
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/complaint_system/results/mobile_interface_mockup.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Mobile interface mockup saved")
    plt.close()


def create_dashboard_mockup():
    """Create a mockup of the admin dashboard"""
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Dashboard background
    bg = Rectangle((0, 0), 16, 10, facecolor='#ecf0f1')
    ax.add_patch(bg)
    
    # Top bar
    topbar = Rectangle((0, 9), 16, 1, facecolor='#2c3e50')
    ax.add_patch(topbar)
    ax.text(0.5, 9.5, '🏛️ Admin Dashboard', ha='left', va='center', 
           fontsize=16, weight='bold', color='white')
    ax.text(15.5, 9.5, 'Logout', ha='right', va='center', 
           fontsize=11, color='white')
    
    # Sidebar
    sidebar = Rectangle((0, 0), 2.5, 9, facecolor='#34495e')
    ax.add_patch(sidebar)
    
    menu_items = ['📊 Overview', '📝 Complaints', '🏢 Departments', '📈 Analytics', '⚙️ Settings']
    menu_y = 8
    for item in menu_items:
        ax.text(0.3, menu_y, item, ha='left', va='center', 
               fontsize=11, color='white', weight='bold')
        menu_y -= 1.5
    
    # Main content area
    ax.text(9.25, 8.3, 'Complaint Management Dashboard', ha='center', va='center', 
           fontsize=18, weight='bold', color='#2c3e50')
    
    # Statistics cards
    stats = [
        ('Total Complaints', '156', '#3498db'),
        ('Pending', '42', '#f39c12'),
        ('In Progress', '67', '#9b59b6'),
        ('Resolved', '47', '#2ecc71')
    ]
    
    card_x = 3.5
    for label, value, color in stats:
        card = FancyBboxPatch((card_x, 6.8), 2.5, 1.2, boxstyle="round,pad=0.1",
                             edgecolor=color, facecolor='white', linewidth=3)
        ax.add_patch(card)
        ax.text(card_x + 1.25, 7.6, value, ha='center', va='center', 
               fontsize=20, weight='bold', color=color)
        ax.text(card_x + 1.25, 7.1, label, ha='center', va='center', 
               fontsize=10, color='#7f8c8d')
        card_x += 3
    
    # Recent complaints table
    table_box = FancyBboxPatch((3, 2), 12.5, 4.3, boxstyle="round,pad=0.1",
                              edgecolor='#bdc3c7', facecolor='white', linewidth=2)
    ax.add_patch(table_box)
    
    ax.text(9.25, 5.9, 'Recent Complaints', ha='center', va='center', 
           fontsize=14, weight='bold', color='#2c3e50')
    
    # Table header
    header_y = 5.4
    headers = ['ID', 'Title', 'Category', 'Priority', 'Status', 'Action']
    header_x = [3.5, 5, 8, 10.5, 12, 13.5]
    
    for x, header in zip(header_x, headers):
        ax.text(x, header_y, header, ha='left', va='center', 
               fontsize=10, weight='bold', color='#2c3e50')
    
    # Table rows
    rows = [
        ('001', 'Water Supply', 'Water', 'High', 'Pending'),
        ('002', 'Road Damage', 'Road', 'Medium', 'In Progress'),
        ('003', 'Power Cut', 'Electricity', 'Low', 'Resolved')
    ]
    
    row_y = 4.9
    for row_data in rows:
        for x, data in zip(header_x, row_data):
            ax.text(x, row_y, data, ha='left', va='center', 
                   fontsize=9, color='#34495e')
        
        # Action button
        action_btn = FancyBboxPatch((13.5, row_y - 0.15), 1.2, 0.3, 
                                   boxstyle="round,pad=0.02",
                                   edgecolor='#3498db', facecolor='#3498db', linewidth=1)
        ax.add_patch(action_btn)
        ax.text(14.1, row_y, 'View', ha='center', va='center', 
               fontsize=8, weight='bold', color='white')
        
        row_y -= 0.7
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/complaint_system/results/dashboard_mockup.png', 
               dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Dashboard mockup saved")
    plt.close()


if __name__ == "__main__":
    print("\n" + "="*70)
    print("GENERATING UI MOCKUP SCREENSHOTS")
    print("="*70 + "\n")
    
    create_web_interface_mockup()
    create_mobile_interface_mockup()
    create_dashboard_mockup()
    
    print("\n" + "="*70)
    print("ALL UI MOCKUPS GENERATED SUCCESSFULLY")
    print("="*70)

