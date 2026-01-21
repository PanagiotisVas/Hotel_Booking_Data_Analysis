import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector

plot_frame = None
stat_buttons = []
column_index = 1

# Στατιστικά Στοιχεία κρατήσεων
def booking_statistics(data, hotel_name):
    filtered_data = data[data['hotel'] == hotel_name]

    hotel_stats = filtered_data.agg({
        'stays_in_weekend_nights': 'mean',
        'stays_in_week_nights': 'mean',
        'is_canceled': lambda x: (x == 1).mean() * 100
    })

    # Δημιουργία διαγράμματος
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['blue', 'green', 'red']
    hotel_stats.plot(kind='bar', rot=0, color=colors, ax=ax)
    ax.set_title(f'{hotel_name} Booking Statistics')
    ax.set_xlabel('Hotel')
    ax.set_ylabel('Average Nights / Cancellation Rate (%)')
    ax.grid(True)

    legend_labels = ['Avg Weekend Nights', 'Avg Week Nights', 'Cancellation Rate']
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors]
    ax.legend(legend_handles, legend_labels)

    return fig, hotel_stats

# Κατανομή κρατήσεων ανά μήνα και ανά εποχή
def bookings_per_month_season(data, hotel_name):
    filtered_data = data[data['hotel'] == hotel_name]

    monthly_bookings = filtered_data['arrival_date_month'].value_counts().sort_index()
    seasonal_bookings = filtered_data['arrival_date_month'].map({
        'January': 'Winter', 'February': 'Winter', 'March': 'Spring',
        'April': 'Spring', 'May': 'Spring', 'June': 'Summer',
        'July': 'Summer', 'August': 'Summer', 'September': 'Fall',
        'October': 'Fall', 'November': 'Winter', 'December': 'Winter'
    }).value_counts().sort_index()

    #Δημιουργία διαγράμματος
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    monthly_bookings.plot(kind='bar', rot=45, color='skyblue', ax=axes[0])
    axes[0].set_title(f'{hotel_name} Monthly Bookings')
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel('Number of Bookings')
    axes[0].grid(True)

    seasonal_bookings.plot(kind='bar', rot=0, color='lightgreen', ax=axes[1])
    axes[1].set_title(f'{hotel_name} Seasonal Bookings')
    axes[1].set_xlabel('Season')
    axes[1].set_ylabel('Number of Bookings')
    axes[1].grid(True)

    plt.tight_layout()
    return fig, monthly_bookings, seasonal_bookings

# Κατανομή των κρατήσεων ανά τύπο δωματίου
def room_type_distribution(data, hotel_name):
    filtered_data = data[data['hotel'] == hotel_name]
    room_type_dist = filtered_data['reserved_room_type'].value_counts()

    # Δημιουργία διαγράμματος
    fig, ax = plt.subplots(figsize=(10, 5))
    room_type_dist.plot(kind='bar', rot=0, color='salmon', ax=ax)
    ax.set_title(f'{hotel_name} Room Type Distribution')
    ax.set_xlabel('Room Type')
    ax.set_ylabel('Number of Bookings')
    ax.grid(True)

    return fig, room_type_dist

# Κρατήσεις ανά είδος πελάτη (οικογένειες, ζευγάρια ή μεμονωμένους ταξιδιώτες)
def guest_type_distribution(data, hotel_name):
    filtered_data = data[data['hotel'] == hotel_name]
    guest_type_dist = filtered_data['customer_type'].value_counts()

    # Δημιουργία διαγράμματος
    fig, ax = plt.subplots(figsize=(10, 5))
    guest_type_dist.plot(kind='bar', rot=0, color='purple', ax=ax)
    ax.set_title(f'{hotel_name} Guest Type Distribution')
    ax.set_xlabel('Guest Type')
    ax.set_ylabel('Number of Bookings')
    ax.grid(True)

    return fig, guest_type_dist

# Τάσεις κρατήσεων με την πάροδο του χρόνου
def booking_trends_over_time(data, hotel_name):
    filtered_data = data[data['hotel'] == hotel_name]
    filtered_data['arrival_date_month'] = pd.to_datetime(filtered_data['arrival_date_month'], format='%B')
    monthly_bookings = filtered_data.groupby('arrival_date_month').size()

    # Δημιουργία διαγράμματος
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_bookings.plot(color='orange', marker='o', linestyle='-', linewidth=2, ax=ax)
    ax.set_title(f'{hotel_name} Booking Trends Over Time')
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Bookings')
    ax.grid(True)
    plt.xticks(rotation=45)

    plt.tight_layout()
    return fig, monthly_bookings

# Εποχικότητα στις κρατήσεις και στις ακυρώσεις
def seasonal_trends(data, hotel_name):
    filtered_data = data[data['hotel'] == hotel_name]

    monthly_book = filtered_data.groupby('arrival_date_month').size()
    monthly_cancel = filtered_data[filtered_data['is_canceled'] == 1].groupby('arrival_date_month').size()

    # Δημιουργία διαγράμματος
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    monthly_book.plot(color='yellow', marker='o', linestyle='-', linewidth=2, ax=axes[0])
    axes[0].set_title(f'{hotel_name} Seasonal Booking Trends')
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel('Number of Bookings')
    axes[0].grid(True)
    plt.xticks(rotation=45)

    monthly_cancel.plot(color='brown', marker='o', linestyle='-', linewidth=2, ax=axes[1])
    axes[1].set_title(f'{hotel_name} Seasonal Cancellation Trends')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Number of Cancellations')
    axes[1].grid(True)
    plt.xticks(rotation=45)

    plt.tight_layout()
    return fig, monthly_book, monthly_cancel

# Γίνεται το export των στοιχείων σε csv αρχεία και η αποθήκευσή τους σε αντίστοιχους πίνακες σε βάση δεδομένων MySQL
def export_and_save_statistics(data, hotel_name, selected_query):

    # Σύνδεση στη βάση δεδομένων MySQL
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='Hotel_booking_analysis'
    )
    cursor = connection.cursor()

    # Εκτέλεση του κάθε ερωτήματος αντίστοιχα
    if selected_query == "Booking Statistics":
        fig, stats = booking_statistics(data, hotel_name)

        sql_query = """INSERT INTO booking_statistics (hotel_name, avg_weekend_nights, avg_week_nights, cancellation_rate) VALUES (%s, %s, %s, %s) """
        values = (hotel_name, stats['stays_in_weekend_nights'], stats['stays_in_week_nights'], stats['is_canceled'])

        # Εκτέλεση της εντολής SQL
        cursor.execute(sql_query, values)
        # Εφαρμογή των αλλαγών στη βάση δεδομένων
        connection.commit()

        stats.to_csv(f"{hotel_name}_booking_statistics.csv")
        print(f"Booking statistics for {hotel_name} exported successfully.")

    elif selected_query == "Monthly and Seasonal Bookings":
        fig, monthly_bookings, seasonal_bookings = bookings_per_month_season(data, hotel_name)

        for month, bookings in monthly_bookings.items():
            sql_query = """INSERT INTO monthly_bookings (hotel_name, month, number_of_bookings) VALUES (%s, %s, %s)"""
            values = (hotel_name, month, bookings)
            cursor.execute(sql_query, values)

        for season, bookings in seasonal_bookings.items():
            sql_query = """INSERT INTO seasonal_bookings (hotel_name, season, number_of_bookings) VALUES (%s, %s, %s)"""
            values = (hotel_name, season, bookings)
            cursor.execute(sql_query, values)

        connection.commit()

        monthly_bookings.to_csv(f"{hotel_name}_monthly_bookings.csv")
        seasonal_bookings.to_csv(f"{hotel_name}_seasonal_bookings.csv")
        print(f"Monthly and seasonal bookings for {hotel_name} exported successfully.")

    elif selected_query == "Room Type Distribution":
        fig, room_type_dist = room_type_distribution(data, hotel_name)

        for room_type, num_bookings in room_type_dist.items():
            sql_query = """INSERT INTO room_type_distribution (hotel_name, room_type, number_of_bookings) VALUES (%s, %s, %s)"""
            values = (hotel_name, room_type, num_bookings)
            cursor.execute(sql_query, values)

        connection.commit()

        room_type_dist.to_csv(f"{hotel_name}_room_type_distribution.csv")
        print(f"Room type distribution for {hotel_name} exported successfully.")

    elif selected_query == "Guest Type Distribution":
        fig, guest_type_dist = guest_type_distribution(data, hotel_name)

        for guest_type, num_bookings in guest_type_dist.items():
            sql_query = """INSERT INTO guest_type_distribution (hotel_name, guest_type, number_of_bookings) VALUES (%s, %s, %s)"""
            values = (hotel_name, guest_type, num_bookings)
            cursor.execute(sql_query, values)

        connection.commit()

        guest_type_dist.to_csv(f"{hotel_name}_guest_type_distribution.csv")
        print(f"Guest type distribution for {hotel_name} exported successfully.")

    elif selected_query == "Booking Trends Over Time":
        fig, monthly_booking_trends = booking_trends_over_time(data, hotel_name)

        for date, num_bookings in monthly_booking_trends.items():
            sql_query = """INSERT INTO booking_trends_over_time (hotel_name, date, number_of_bookings) VALUES (%s, %s, %s)"""
            values = (hotel_name, date, num_bookings)
            cursor.execute(sql_query, values)

        connection.commit()

        monthly_booking_trends.to_csv(f"{hotel_name}_booking_trends_over_time.csv")
        print(f"Booking trends over time for {hotel_name} exported successfully.")

    elif selected_query == "Seasonal Trends":
        fig, seasonal_book, seasonal_cancel = seasonal_trends(data, hotel_name)

        for month, num_bookings in seasonal_book.items():
            sql_query = """INSERT INTO seasonal_booking_trends (hotel_name, month, number_of_bookings) VALUES (%s, %s, %s)"""
            values = (hotel_name, month, num_bookings)
            cursor.execute(sql_query, values)

        for month, num_cancellations in seasonal_cancel.items():
            sql_query = """INSERT INTO seasonal_cancellation_trends (hotel_name, month, number_of_cancellations) VALUES (%s, %s, %s)"""
            values = (hotel_name, month, num_cancellations)
            cursor.execute(sql_query, values)

        connection.commit()

        seasonal_book.to_csv(f"{hotel_name}_seasonal_booking_trends.csv")
        seasonal_cancel.to_csv(f"{hotel_name}_seasonal_cancellation_trends.csv")
        print(f"Seasonal trends for {hotel_name} exported successfully.")

    else:
        print("Invalid query selected or no statistics generated.")

# Δημιουργία της Γραφικής Διεπαφής
def create_gui(data):

    current_plot = None  # Μεταβλητή για το τρέχον διάγραμμα

    def display_stats(stat_func, hotel_name):
        nonlocal current_plot

        if current_plot is not None:
            current_plot.get_tk_widget().pack_forget()  # Απομάκρυνση του τρέχοντος διαγράμματος

        plot = stat_func(data, hotel_name)
        if isinstance(plot, tuple):
            plot = plot[0]
        canvas = FigureCanvasTkAgg(plot, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0, rowspan=4, columnspan=8, pady=10, padx=10, sticky="nsew")

        current_plot = canvas  # Αποθήκευση του νέου διαγράμματος στην current_plot

    def update_buttons(selected_hotel):
        # Ενημέρωση των κουμπιών με βάση το επιλεγμένο ξενοδοχείο
        global stat_buttons
        nonlocal current_plot
        global column_index

        for button in stat_buttons:
            button.pack_forget()  # Διεγραφή των προηγούμενων κουμπιών

            # Δημιουργία και τοποθέτηση νέων κουμπιών χρησιμοποιώντας τη grid()
            column_index = 1  # Αρχίζουμε από τη γραμμή 1 για να αποφευχθεί η κάλυψη του Combobox

        statistics_functions = [
            (booking_statistics, "Booking Statistics"),
            (bookings_per_month_season, "Monthly and Seasonal Bookings"),
            (room_type_distribution, "Room Type Distribution"),
            (guest_type_distribution, "Guest Type Distribution"),
            (booking_trends_over_time, "Booking Trends Over Time"),
            (seasonal_trends, "Seasonal Trends")
        ]

        for stat_func, button_text in statistics_functions:
            button = ttk.Button(button_frame, text=button_text, command=lambda func=stat_func: display_stats(func, selected_hotel))
            button.grid(row=1, column=column_index, pady=10, padx=10, sticky="nsew")
            stat_buttons.append(button)
            column_index += 1

    def add_export_button():

        # Λίστα με τα ερωτήματα
        queries = ["Booking Statistics", "Monthly and Seasonal Bookings", "Room Type Distribution",
                   "Guest Type Distribution", "Booking Trends Over Time", "Seasonal Trends"]

        selected_query = tk.StringVar(root)
        selected_query.set(queries[0])  # Αρχική τιμή του combobox

        def export_and_save_selected_statistics():
            # Εξαγωγή των επιλεγμένων στατιστικών
            data = pd.read_csv("hotel_booking.csv")
            hotel_name = hotel_combobox.get()
            selected_query_value = selected_query.get()

            export_and_save_statistics(data, hotel_name, selected_query_value)


        export_button = ttk.Button(button_frame, text="Export/Save", command=export_and_save_selected_statistics)
        export_button.grid(row=0, column=6, padx=10, pady=10, sticky="nsew")

        dropdown_menu = tk.OptionMenu(button_frame, selected_query, *queries)
        dropdown_menu.grid(row=0, column=5, padx=10, pady=10, sticky="nsew")

    def hotel_selected(event):
        global plot_frame
        global stat_buttons

        selected_hotel = hotel_combobox.get()

        if plot_frame is not None:
           plot_frame.destroy()

        plot_frame = tk.Frame(root)
        plot_frame.grid(row=2, column=2, pady=20, padx=10, sticky="nsew")

        # Ενημέρωση των κουμπιών με το επιλεγμένο ξενοδοχείο
        update_buttons(selected_hotel)

        # Επαναφορά της current_plot σε None όταν επιλέγεται νέο ξενοδοχείο
        nonlocal current_plot
        current_plot = None

    root = tk.Tk()
    root.title("Hotel Booking Analysis  |  Developed by Vasilopoulos Panagiotis - CEID, University of Patras - 2024")
    root.geometry("1100x700")  # Ορίζει το παράθυρο με πλάτος 1100 pixels και ύψος 700 pixels

    # Ορίζουμε το στυλ για τα ttk widgets
    style = ttk.Style()
    style.configure('Frame1.TFrame', background='#333333')  # Χρώμα φόντου για το root
    style.configure('Frame2.TFrame', background='black')  # Χρώμα φόντου για το button_frame
    style.configure('TLabel', background='black', foreground='white')  # Χρώμα κειμένου για ετικέτα του combobox

    # Ορισμός του χρώματος φόντου του root
    root.configure(background=style.lookup('Frame1.TFrame', 'background'))

    # Frame για τα κουμπιά με στατιστικά
    button_frame = ttk.Frame(root, padding=(10, 10, 10, 10), style='Frame2.TFrame')
    button_frame.grid(row=0, column=0, rowspan=2, columnspan=6, pady=10, padx=10, sticky="nsew")

    hotel_label = ttk.Label(button_frame, text="Select Hotel:", style='TLabel')
    hotel_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

    hotels = ['Resort Hotel', 'City Hotel']
    hotel_combobox = ttk.Combobox(button_frame, values=hotels, width=65)
    hotel_combobox.grid(row=0, column=1, columnspan=3, pady=10, padx=10, sticky="nsew")

    hotel_combobox.bind("<<ComboboxSelected>>", hotel_selected)

    add_export_button()

    root.mainloop()


def main():
    # Load the dataset
    file_path = "hotel_booking.csv"
    data = pd.read_csv(file_path)

    # Δημιουργία του GUI
    create_gui(data)

if __name__ == "__main__":
    main()
