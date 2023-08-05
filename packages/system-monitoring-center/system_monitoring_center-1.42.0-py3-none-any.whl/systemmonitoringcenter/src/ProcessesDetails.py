#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, Gdk, GLib
import os
import time
from datetime import datetime
import subprocess

from locale import gettext as _tr

from Config import Config
import Processes
from Performance import Performance


class ProcessesDetails:

    def __init__(self, selected_process_pid):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesDetailsWindow.ui")

        # Get GUI objects
        self.window2101w = builder.get_object('window2101w')
        self.grid2101w = builder.get_object('grid2101w')
        self.notebook2101w = builder.get_object('notebook2101w')
        # Get "Summary" tab GUI objects
        self.label2101w = builder.get_object('label2101w')
        self.label2102w = builder.get_object('label2102w')
        self.label2103w = builder.get_object('label2103w')
        self.label2104w = builder.get_object('label2104w')
        self.label2105w = builder.get_object('label2105w')
        self.label2106w = builder.get_object('label2106w')
        self.label2107w = builder.get_object('label2107w')
        self.label2108w = builder.get_object('label2108w')
        self.label2109w = builder.get_object('label2109w')
        self.label2110w = builder.get_object('label2110w')
        self.label2111w = builder.get_object('label2111w')
        self.label2114w = builder.get_object('label2114w')
        self.label2115w = builder.get_object('label2115w')
        self.label2138w = builder.get_object('label2138w')
        # Get "CPU" tab GUI objects
        self.drawingarea2101w = builder.get_object('drawingarea2101w')
        self.label2116w = builder.get_object('label2116w')
        self.label2117w = builder.get_object('label2117w')
        self.label2118w = builder.get_object('label2118w')
        self.label2119w = builder.get_object('label2119w')
        self.label2121w = builder.get_object('label2121w')
        self.label2122w = builder.get_object('label2122w')
        # Get "RAM" tab GUI objects
        self.drawingarea2102w = builder.get_object('drawingarea2102w')
        self.label2123w = builder.get_object('label2123w')
        self.label2124w = builder.get_object('label2124w')
        self.label2125w = builder.get_object('label2125w')
        self.label2126w = builder.get_object('label2126w')
        self.label2127w = builder.get_object('label2127w')
        self.label2139w = builder.get_object('label2139w')
        # Get "Disk" tab GUI objects
        self.drawingarea2103w = builder.get_object('drawingarea2103w')
        self.label2128w = builder.get_object('label2128w')
        self.label2129w = builder.get_object('label2129w')
        self.label2130w = builder.get_object('label2130w')
        self.label2131w = builder.get_object('label2131w')
        self.label2132w = builder.get_object('label2132w')
        self.label2133w = builder.get_object('label2133w')
        self.label2140w = builder.get_object('label2140w')
        # Get "Path" tab GUI objects
        self.label2134w = builder.get_object('label2134w')
        self.label2135w = builder.get_object('label2135w')
        self.label2136w = builder.get_object('label2136w')
        self.label2137w = builder.get_object('label2137w')

        # Get chart functions from another module and define as local objects for lower CPU usage.
        self.performance_line_charts_draw_func = Performance.performance_line_charts_draw_func
        self.performance_line_charts_enter_notify_event_func = Performance.performance_line_charts_enter_notify_event_func
        self.performance_line_charts_leave_notify_event_func = Performance.performance_line_charts_leave_notify_event_func
        self.performance_line_charts_motion_notify_event_func = Performance.performance_line_charts_motion_notify_event_func

        # Connect GUI signals
        self.window2101w.connect("delete-event", self.on_window2101w_delete_event)
        self.window2101w.connect("show", self.on_window2101w_show)

        self.drawingarea2101w.connect("draw", self.performance_line_charts_draw_func)
        self.drawingarea2101w.connect("enter-notify-event", self.performance_line_charts_enter_notify_event_func)
        self.drawingarea2101w.connect("leave-notify-event", self.performance_line_charts_leave_notify_event_func)
        self.drawingarea2101w.connect("motion-notify-event", self.performance_line_charts_motion_notify_event_func)

        self.drawingarea2102w.connect("draw", self.performance_line_charts_draw_func)
        self.drawingarea2102w.connect("enter-notify-event", self.performance_line_charts_enter_notify_event_func)
        self.drawingarea2102w.connect("leave-notify-event", self.performance_line_charts_leave_notify_event_func)
        self.drawingarea2102w.connect("motion-notify-event", self.performance_line_charts_motion_notify_event_func)

        self.drawingarea2103w.connect("draw", self.performance_line_charts_draw_func)
        self.drawingarea2103w.connect("enter-notify-event", self.performance_line_charts_enter_notify_event_func)
        self.drawingarea2103w.connect("leave-notify-event", self.performance_line_charts_leave_notify_event_func)
        self.drawingarea2103w.connect("motion-notify-event", self.performance_line_charts_motion_notify_event_func)


        # Set event masks for drawingarea in order to enable these events.
        self.drawingarea2101w.set_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK | Gdk.EventMask.POINTER_MOTION_MASK)
        self.drawingarea2102w.set_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK | Gdk.EventMask.POINTER_MOTION_MASK)
        self.drawingarea2103w.set_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK | Gdk.EventMask.POINTER_MOTION_MASK)


        # Get selected_process_pid for using it for the current process object instance.
        self.selected_process_pid = selected_process_pid


    # ----------------------- Called for running code/functions when window is closed -----------------------
    def on_window2101w_delete_event(self, widget, event):

        self.update_window_value = 0
        self.window2101w.hide()
        # Remove the current process object instance from the list if the window is closed.
        processes_details_object_list.remove(self)
        # Delete the current process object instance if the window is closed.
        del self
        return True


    # ----------------------- Called for running code/functions when GUI is shown -----------------------
    def on_window2101w_show(self, widget):

        try:
            # Delete "update_interval" variable in order to let the code to run initial function. Otherwise, data from previous process (if it was viewed) will be used.
            del self.update_interval
        except AttributeError:
            pass

        # Delete first row of the grid and widget in it if it is a label. This widget can be a label if a process is ended when its window is opened. An information label is added into the first row of the grid in this situation and it stays here if a window of another process is opened.
        widget_in_first_row = self.grid2101w.get_child_at(0, 0)
        widget_name_in_first_row = widget_in_first_row.get_name()
        if widget_name_in_first_row == "GtkLabel":
            self.grid2101w.remove_row(0)
            widget_in_first_row.destroy()

        # This value is checked for repeating the function for getting the process data.
        self.update_window_value = 1

        # Call this function in order to reset Processes Details window GUI.
        self.processes_details_gui_reset_function()
        self.process_details_run_func()


    # ----------------------- Called for resetting window GUI -----------------------
    def processes_details_gui_reset_function(self):

        # Set fist page (Summary tab) of the notebook
        self.notebook2101w.set_current_page(0)

        self.label2101w.set_text("--")
        self.label2102w.set_text("--")
        self.label2103w.set_text("--")
        self.label2104w.set_text("--")
        self.label2105w.set_text("--")
        self.label2106w.set_text("--")
        self.label2107w.set_text("--")
        self.label2108w.set_text("--")
        self.label2109w.set_text("--")
        self.label2110w.set_text("--")
        self.label2111w.set_text("--")
        self.label2114w.set_text("--")
        self.label2115w.set_text("--")
        self.label2116w.set_text("--")
        self.label2117w.set_text("--")
        self.label2118w.set_text("--")
        self.label2119w.set_text("--")
        self.label2121w.set_text("--")
        self.label2122w.set_text("--")
        self.label2123w.set_text("--")
        self.label2124w.set_text("--")
        self.label2125w.set_text("--")
        self.label2126w.set_text("--")
        self.label2127w.set_text("--")
        self.label2128w.set_text("--")
        self.label2129w.set_text("--")
        self.label2130w.set_text("--")
        self.label2131w.set_text("--")
        self.label2132w.set_text("--")
        self.label2133w.set_text("--")
        self.label2134w.set_text("--")
        self.label2135w.set_text("--")
        self.label2136w.set_text("--")
        self.label2137w.set_text("--")
        self.label2138w.set_text("--")
        self.label2139w.set_text("--")
        self.label2140w.set_text("--")


    # ----------------------------------- Processes - Processes Details Function -----------------------------------
    def process_details_initial_func(self):

        # Define data unit conversion function objects in for lower CPU usage.
        self.performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        self.performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        self.performance_define_data_unit_converter_variables_func()

        self.process_status_list = Processes.process_status_list
        self.global_process_cpu_times_prev = []
        self.disk_read_write_data_prev = []

        chart_data_history = Config.chart_data_history

        self.process_cpu_usage_list = [0] * chart_data_history
        self.process_ram_usage_list = [0] * chart_data_history
        self.process_disk_read_speed_list = [0] * chart_data_history
        self.process_disk_write_speed_list = [0] * chart_data_history

        # Get system boot time.
        with open("/proc/stat") as reader:
            stat_lines = reader.read().split("\n")
        for line in stat_lines:
            if "btime " in line:
                self.system_boot_time = int(line.split()[1].strip())

        self.number_of_clock_ticks = Processes.number_of_clock_ticks


    # ----------------------------------- Processes - Processes Details Foreground Function -----------------------------------
    def process_details_loop_func(self):

        processes_cpu_precision = Config.processes_cpu_precision
        processes_memory_data_precision = Config.processes_memory_data_precision
        processes_memory_data_unit = Config.processes_memory_data_unit
        processes_disk_data_precision = Config.processes_disk_data_precision
        processes_disk_data_unit = Config.processes_disk_data_unit
        processes_disk_speed_bit = Config.processes_disk_speed_bit

        # Get "selected_process_pid".
        selected_process_pid = self.selected_process_pid

        # Get information.
        usernames_username_list, usernames_uid_list = self.processes_details_usernames_uids_func()
        stat_output, status_output, statm_output, io_output, smaps_output, cmdline_output = self.processes_details_stat_status_statm_io_smaps_cmdline_outputs_func(selected_process_pid)
        if stat_output == "-" or status_output == "-" or statm_output == "-":
            self.update_window_value = 0
            self.process_details_process_end_label_func()
            return
        global_cpu_time_all = self.process_details_global_cpu_time_func()
        stat_output_split = stat_output.split()
        status_output_split = status_output.split("\n")
        io_output_lines = io_output.split("\n")
        fd_ls_output, task_ls_output = self.processes_details_fd_task_ls_output_func(selected_process_pid)
        if task_ls_output == "-":
            self.update_window_value = 0
            self.process_details_process_end_label_func()
            return
        selected_process_name = self.process_details_process_name_func(selected_process_pid, stat_output, cmdline_output)
        selected_process_username = self.process_details_process_user_name_func(selected_process_pid, status_output_split, usernames_username_list, usernames_uid_list)
        selected_process_status = self.process_details_process_status_func(stat_output_split)
        selected_process_nice = self.process_details_process_nice_func(stat_output_split)
        selected_process_cpu_percent = self.process_details_process_cpu_usage_func(stat_output_split, global_cpu_time_all)
        selected_process_memory_rss = self.process_details_process_memory_rss_func(stat_output_split)
        selected_process_read_bytes, selected_process_write_bytes = self.process_details_process_disk_read_write_data_func(io_output_lines)
        selected_process_read_speed, selected_process_write_speed = self.process_details_process_disk_read_write_speed_func(selected_process_read_bytes, selected_process_write_bytes)
        selected_process_start_time = self.process_details_process_start_time_func(stat_output_split)
        selected_process_ppid = self.process_details_process_ppid_func(stat_output_split)
        selected_process_uid_real, selected_process_uid_effective, selected_process_uid_saved = self.process_details_process_real_effective_saved_uids_func(status_output_split)
        selected_process_gid_real, selected_process_gid_effective, selected_process_gid_saved = self.process_details_process_real_effective_saved_gids_func(status_output_split)
        selected_process_num_threads = self.process_details_process_number_of_threads_func(stat_output_split)
        selected_process_threads = self.process_details_process_tids_func(task_ls_output)
        selected_process_cpu_num = self.process_details_process_cpu_number_func(stat_output_split)
        selected_process_cpu_times_user, selected_process_cpu_times_kernel, selected_process_cpu_times_children_user, selected_process_cpu_times_children_kernel, selected_process_cpu_times_io_wait = self.process_details_process_cpu_times_func(stat_output_split)
        selected_process_num_ctx_switches_voluntary, selected_process_num_ctx_switches_nonvoluntary = self.process_details_process_context_switches_func(status_output_split)
        selected_process_memory_vms = self.process_details_process_memory_vms_func(stat_output_split)
        selected_process_memory_shared = self.process_details_process_memory_shared_func(statm_output)
        selected_process_memory_uss, selected_process_memory_swap = self.process_details_process_memory_uss_and_swap_func(smaps_output)
        selected_process_read_count, selected_process_write_count = self.process_details_process_read_write_counts_func(io_output_lines)
        selected_process_cmdline = self.process_details_process_cmdline_func(cmdline_output)
        selected_process_exe, selected_process_cwd, selected_process_open_files = self.process_details_process_exe_cwd_open_files_func(selected_process_pid, fd_ls_output)

        # Stop running functions in order to prevent errors.
        if self.update_window_value == 0:
            return

        # Set window title
        self.window2101w.set_title(_tr("Process Details") + ":  " + selected_process_name + " - (" + _tr("PID") + ": " + selected_process_pid + ")")

        # Update data lists for graphs.
        self.process_cpu_usage_list.append(selected_process_cpu_percent)
        del self.process_cpu_usage_list[0]
        self.process_ram_usage_list.append(selected_process_memory_rss)
        del self.process_ram_usage_list[0]
        self.process_disk_read_speed_list.append(selected_process_read_speed)
        del self.process_disk_read_speed_list[0]
        self.process_disk_write_speed_list.append(selected_process_write_speed)
        del self.process_disk_write_speed_list[0]

        # Update graphs.
        self.drawingarea2101w.queue_draw()
        self.drawingarea2102w.queue_draw()
        self.drawingarea2103w.queue_draw()

        # Show information on labels (Summary tab).
        self.label2101w.set_text(selected_process_name)
        self.label2102w.set_text(f'{selected_process_pid}')
        self.label2103w.set_text(selected_process_status)
        self.label2104w.set_text(selected_process_username)
        self.label2105w.set_text(f'{selected_process_nice}')
        self.label2106w.set_text(f'{selected_process_cpu_percent:.{processes_cpu_precision}f} %')
        self.label2107w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_memory_rss, processes_memory_data_unit, processes_memory_data_precision)}')
        if selected_process_read_bytes != "-":
            self.label2108w.set_text(f'{self.performance_data_unit_converter_func("speed", processes_disk_speed_bit, selected_process_read_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
        if selected_process_read_bytes == "-":
            self.label2108w.set_text("-")
        if selected_process_write_bytes != "-":
            self.label2138w.set_text(f'{self.performance_data_unit_converter_func("speed", processes_disk_speed_bit, selected_process_write_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
        if selected_process_write_bytes == "-":
            self.label2138w.set_text("-")
        self.label2109w.set_text(datetime.fromtimestamp(selected_process_start_time).strftime("%d.%m.%Y %H:%M:%S"))
        self.label2110w.set_text(selected_process_exe)
        self.label2111w.set_text(f'{selected_process_ppid}')
        self.label2114w.set_text(f'Real: {selected_process_uid_real}, Effective: {selected_process_uid_effective}, Saved: {selected_process_uid_saved}')
        self.label2115w.set_text(f'Real: {selected_process_gid_real}, Effective: {selected_process_gid_effective}, Saved: {selected_process_gid_saved}')

        # Show information on labels (CPU tab).
        self.label2116w.set_text(f'{selected_process_cpu_percent:.{processes_cpu_precision}f} %')
        self.label2117w.set_text(f'{selected_process_num_threads}')
        self.label2118w.set_text(',\n'.join(selected_process_threads))
        self.label2119w.set_text(f'{selected_process_cpu_num}')
        self.label2121w.set_text(f'User: {selected_process_cpu_times_user}, System: {selected_process_cpu_times_kernel}, Children User: {selected_process_cpu_times_children_user}, Children System: {selected_process_cpu_times_children_kernel}, IO Wait: {selected_process_cpu_times_io_wait}')
        self.label2122w.set_text(f'Voluntary: {selected_process_num_ctx_switches_voluntary}, Involuntary: {selected_process_num_ctx_switches_nonvoluntary}')

        # Show information on labels (Memory tab).
        self.label2123w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_memory_rss, processes_memory_data_unit, processes_memory_data_precision)}')
        self.label2124w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_memory_vms, processes_memory_data_unit, processes_memory_data_precision)}')
        self.label2125w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_memory_shared, processes_memory_data_unit, processes_memory_data_precision)}')
        if selected_process_memory_uss != "-" and selected_process_memory_swap != "-":
            self.label2126w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_memory_uss, processes_memory_data_unit, processes_memory_data_precision)}')
            self.label2127w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_memory_swap, processes_memory_data_unit, processes_memory_data_precision)}')
        if selected_process_memory_uss == "-" and selected_process_memory_swap == "-":
            self.label2126w.set_text(selected_process_memory_uss)
            self.label2127w.set_text(selected_process_memory_swap)

        # Show information on labels (Disk tab).
        if selected_process_read_bytes != "-" and selected_process_write_bytes != "-":
            self.label2128w.set_text(f'{self.performance_data_unit_converter_func("speed", processes_disk_speed_bit, selected_process_read_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
            self.label2129w.set_text(f'{self.performance_data_unit_converter_func("speed", processes_disk_speed_bit, selected_process_write_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
            self.label2130w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_read_bytes, processes_disk_data_unit, processes_disk_data_precision)}')
            self.label2131w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_write_bytes, processes_disk_data_unit, processes_disk_data_precision)}')
            self.label2132w.set_text(f'{selected_process_read_count}')
            self.label2133w.set_text(f'{selected_process_write_count}')
        if selected_process_read_bytes == "-" and selected_process_write_bytes == "-":
            self.label2128w.set_text("-")
            self.label2129w.set_text("-")
            self.label2130w.set_text("-")
            self.label2131w.set_text("-")
            self.label2132w.set_text("-")
            self.label2133w.set_text("-")

        # Show information on labels (Path tab).
        self.label2134w.set_text(selected_process_exe)
        self.label2135w.set_text(selected_process_cwd)
        self.label2136w.set_text(' '.join(selected_process_cmdline))
        if selected_process_open_files != "-":
            self.label2137w.set_text(',\n'.join(selected_process_open_files))
        if selected_process_open_files == "-":
            self.label2137w.set_text("-")


    # ----------------------------------- Processes Details - Run Function -----------------------------------
    # "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to change the update interval and run the loop again without waiting ending the previous update interval.
    def process_details_run_func(self, *args):

        if hasattr(self, "update_interval") == False:
            GLib.idle_add(self.process_details_initial_func)

        # Destroy GLib source for preventing it repeating the function.
        try:
            self.main_glib_source.destroy()
        # "try-except" is used in order to prevent errors if this is first run of the function.
        except AttributeError:
            pass
        self.update_interval = Config.update_interval
        self.main_glib_source = GLib.timeout_source_new(self.update_interval * 1000)

        if self.update_window_value == 1:
            GLib.idle_add(self.process_details_loop_func)
            self.main_glib_source.set_callback(self.process_details_run_func)
            # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.
            self.main_glib_source.attach(GLib.MainContext.default())


    # ----------------------- Called for showing information label if the process is ended. -----------------------
    def process_details_process_end_label_func(self):

        # Prevent adding more than one label (if there is already a label).
        widget_in_first_row = self.grid2101w.get_child_at(0, 0)
        widget_name_in_first_row = widget_in_first_row.get_name()
        if widget_name_in_first_row == "GtkLabel":
            return

        # Generate a new label for the information. This label does not exist in the ".ui" UI file.
        label_process_end_warning = Gtk.Label(label=_tr("This process is not running anymore."))
        css = b"label {background: rgba(100%,0%,0%,1.0);}"
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        label_process_end_warning.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.grid2101w.insert_row(0)
        # Attach the label to the grid at (0, 0) position.
        self.grid2101w.attach(label_process_end_warning, 0, 0, 1, 1)
        label_process_end_warning.set_visible(True)


    # ----------------------- Get usernames and UIDs -----------------------
    def processes_details_usernames_uids_func(self):

        usernames_username_list = []
        usernames_uid_list = []
        with open("/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")
        for line in etc_passwd_lines:
            line_splitted = line.split(":")
            usernames_username_list.append(line_splitted[0])
            usernames_uid_list.append(line_splitted[2])

        return usernames_username_list, usernames_uid_list


    # ----------------------- Get stat, status, statm, io, smaps, cmdline file outputs. -----------------------
    def processes_details_stat_status_statm_io_smaps_cmdline_outputs_func(self, selected_process_pid):

        # Generate command for getting file outputs.
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host", "cat"]
        else:
            command_list = ["cat"]
        command_list.append("/proc/version")
        command_list.append("/proc/" + selected_process_pid + "/stat")
        command_list.append("/proc/version")
        command_list.append("/proc/" + selected_process_pid + "/status")
        command_list.append("/proc/version")
        command_list.append("/proc/" + selected_process_pid + "/statm")
        command_list.append("/proc/version")
        command_list.append("/proc/" + selected_process_pid + "/io")
        command_list.append("/proc/version")
        command_list.append("/proc/" + selected_process_pid + "/smaps")
        command_list.append("/proc/version")
        command_list.append("/proc/" + selected_process_pid + "/cmdline")

        cat_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()

        # Get split text by using the first line. This text will be used for splitting
        # the outputs of different procfs files. Because output of some files may be ""
        # and they are not shown in the output of command if multiple files are used as arguments.
        cat_output_lines = cat_output.split("\n")
        split_text = cat_output_lines[0].strip()
        cat_output_split = cat_output.split(split_text)
        del cat_output_split[0]
        # Get output of procfs files.
        stat_output = cat_output_split[0].strip()
        status_output = cat_output_split[1].strip()
        statm_output = cat_output_split[2].strip()
        io_output = cat_output_split[3].strip()
        smaps_output = cat_output_split[4].strip()
        cmdline_output = cat_output_split[5].strip().replace("\x00", " ")                     # "\x00" characters in "cmdline" file are replaced with " ".

        if stat_output == "":
            stat_output = "-"
        if status_output == "":
            status_output = "-"
        if statm_output == "":
            statm_output = "-"
        if io_output == "":
            io_output = "-"
        if smaps_output == "":
            smaps_output = "-"
        if cmdline_output == "":
            cmdline_output = "-"

        return stat_output, status_output, statm_output, io_output, smaps_output, cmdline_output


    # ----------------------- Get fd and stat folder list outputs. -----------------------
    def processes_details_fd_task_ls_output_func(self, selected_process_pid):

        # Generate command for getting file outputs.
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host", "ls"]
        else:
            command_list = ["ls"]
        command_list.append("/proc/" + selected_process_pid + "/fd/")
        command_list.append("/proc/" + selected_process_pid + "/task/")

        ls_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()

        # Get output of procfs folders.
        if "/fd/" in ls_output and "/task/" in ls_output:
            fd_ls_output, task_ls_output = ls_output.split("\n\n")
        elif "/fd/" in ls_output and "/task/" not in ls_output:
            fd_ls_output = ls_output
            task_ls_output = "-"
        elif "/fd/" not in ls_output and "/task/" in ls_output:
            fd_ls_output = "-"
            task_ls_output = ls_output
        else:
            fd_ls_output = "-"
            task_ls_output = "-"

        return fd_ls_output, task_ls_output


    # ----------------------- Get global CPU time -----------------------
    def process_details_global_cpu_time_func(self):

        # global_cpu_time_all value is get just after "/proc/[PID]/stat file is
        # read in order to measure global an process specific CPU times at the
        # same time (nearly) for ensuring accurate process CPU usage percent.
        global_cpu_time_all = time.time() * self.number_of_clock_ticks

        return global_cpu_time_all


    # ----------------------- Get process name -----------------------
    def process_details_process_name_func(self, selected_process_pid, stat_output, cmdline_output):

        first_parentheses = stat_output.find("(")                                             # Process name is in parantheses and name may include whitespaces (may also include additinl parantheses). First parantheses "(" index is get by using "find()".
        second_parentheses = stat_output.rfind(")")                                           # Last parantheses ")" index is get by using "find()".
        process_name_from_stat = stat_output[first_parentheses+1:second_parentheses]          # Process name is get from string by using the indexes get previously.
        selected_process_name = process_name_from_stat

        if len(selected_process_name) == 15:                                                  # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character (not all process cmdlines have this) in order to obtain full process name.
            selected_process_name = cmdline_output.split("/")[-1].split(" ")[0]
            if selected_process_name.startswith(process_name_from_stat) == False:
                selected_process_name = cmdline_output.split(" ")[0].split("/")[-1]
                if selected_process_name.startswith(process_name_from_stat) == False:
                    selected_process_name = process_name_from_stat

        return selected_process_name


    # ----------------------- Get process user name -----------------------
    def process_details_process_user_name_func(self, selected_process_pid, status_output_split, usernames_username_list, usernames_uid_list):

        for line in status_output_split:
            if "Uid:\t" in line:
                # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                real_user_id = line.split(":")[1].split()[0].strip()
                try:
                    selected_process_username = usernames_username_list[usernames_uid_list.index(real_user_id)]
                except ValueError:
                    selected_process_username = real_user_id

        return selected_process_username


    # ----------------------- Get process status -----------------------
    def process_details_process_status_func(self, stat_output_split):

        selected_process_status = self.process_status_list[stat_output_split[-50]]

        return selected_process_status


    # ----------------------- Get process nice -----------------------
    def process_details_process_nice_func(self, stat_output_split):

        selected_process_nice = int(stat_output_split[-34])

        return selected_process_nice


    # ----------------------- Get process CPU usage -----------------------
    def process_details_process_cpu_usage_func(self, stat_output_split, global_cpu_time_all):

        # Get process cpu time in user mode (utime + stime)
        process_cpu_time = int(stat_output_split[-39]) + int(stat_output_split[-38])
        global_process_cpu_times = [global_cpu_time_all, process_cpu_time]
        try:
            global_cpu_time_all_prev, process_cpu_time_prev = self.global_process_cpu_times_prev
        # It gives various errors (ValueError, IndexError, UnboundLocalError) if a new process is started, a new column is shown on the treeview, etc because previous CPU time values are not present in these situations. Following CPU time values are used in these situations.
        except (ValueError, IndexError, UnboundLocalError) as me:
            process_cpu_time_prev = process_cpu_time                                      # There is no "process_cpu_time_prev" value and get it from "process_cpu_time" if this is first loop of the process.
            global_cpu_time_all_prev = global_process_cpu_times[0] - 1                    # Subtract "1" CPU time (a negligible value) if this is first loop of the process.
        process_cpu_time_difference = process_cpu_time - process_cpu_time_prev
        global_cpu_time_difference = global_cpu_time_all - global_cpu_time_all_prev
        selected_process_cpu_percent = process_cpu_time_difference / global_cpu_time_difference * 100 / Processes.number_of_logical_cores
        self.global_process_cpu_times_prev = global_process_cpu_times

        return selected_process_cpu_percent


    # ----------------------- Get process memory (RSS) -----------------------
    def process_details_process_memory_rss_func(self, stat_output_split):

        # Get process RSS (resident set size) memory pages and multiply with memory_page_size in order to convert the value into bytes.
        selected_process_memory_rss = int(stat_output_split[-29]) * Processes.memory_page_size

        return selected_process_memory_rss


    # ----------------------- Get process disk read data, disk write data -----------------------
    def process_details_process_disk_read_write_data_func(self, io_output_lines):

        if io_output_lines != ["-"]:
            selected_process_read_bytes = int(io_output_lines[4].split(":")[1])
            selected_process_write_bytes = int(io_output_lines[5].split(":")[1])
        else:
            selected_process_read_bytes = 0
            selected_process_write_bytes = 0

        return selected_process_read_bytes, selected_process_write_bytes


    # ----------------------- Get process disk read speed, disk write speed -----------------------
    def process_details_process_disk_read_write_speed_func(self, selected_process_read_bytes, selected_process_write_bytes):

        # Get disk read speed.
        disk_read_write_data = [selected_process_read_bytes, selected_process_write_bytes]
        if self.disk_read_write_data_prev == []:
            # Make process_read_bytes_prev equal to process_read_bytes for giving "0" disk read speed value if this is first loop of the process.
            selected_process_read_bytes_prev = selected_process_read_bytes
        else:
            selected_process_read_bytes_prev = self.disk_read_write_data_prev[0]
        selected_process_read_speed = (selected_process_read_bytes - int(selected_process_read_bytes_prev)) / self.update_interval

        # Get disk write speed.
        if self.disk_read_write_data_prev == []:
            # Make process_write_bytes_prev equal to process_write_bytes for giving "0" disk write speed value if this is first loop of the process.
            selected_process_write_bytes_prev = selected_process_write_bytes
        else:
            selected_process_write_bytes_prev = self.disk_read_write_data_prev[1]
        selected_process_write_speed = (selected_process_write_bytes - int(selected_process_write_bytes_prev)) / self.update_interval

        self.disk_read_write_data_prev = disk_read_write_data

        return selected_process_read_speed, selected_process_write_speed


    # ----------------------- Get process start time -----------------------
    def process_details_process_start_time_func(self, stat_output_split):

        # Elapsed time between system boot and process start time (measured in clock ticks and need to be divided by sysconf(_SC_CLK_TCK) for converting into wall clock time)
        selected_process_start_time_raw = int(stat_output_split[-31])
        selected_process_start_time = (selected_process_start_time_raw / self.number_of_clock_ticks) + self.system_boot_time

        return selected_process_start_time


    # ----------------------- Get process PPID -----------------------
    def process_details_process_ppid_func(self, stat_output_split):

        selected_process_ppid = int(stat_output_split[-49])

        return selected_process_ppid


    # ----------------------- Get process real, effective and saved UIDs -----------------------
    def process_details_process_real_effective_saved_uids_func(self, status_output_split):

        for line in status_output_split:
            if "Uid:\t" in line:
                line_split = line.split(":")[1].split()
                # There are 4 values in the Uid line (real, effective, user, filesystem UIDs)
                selected_process_uid_real = line_split[0].strip()
                selected_process_uid_effective = line_split[1].strip()
                selected_process_uid_saved = line_split[2].strip()

        return selected_process_uid_real, selected_process_uid_effective, selected_process_uid_saved


    # ----------------------- Get process real, effective and saved GIDs -----------------------
    def process_details_process_real_effective_saved_gids_func(self, status_output_split):

        for line in status_output_split:
            if "Gid:\t" in line:
                line_split = line.split(":")[1].split()
                # There are 4 values in the Gid line (real, effective, user, filesystem GIDs)
                selected_process_gid_real = line_split[0].strip()
                selected_process_gid_effective = line_split[1].strip()
                selected_process_gid_saved = line_split[2].strip()

        return selected_process_gid_real, selected_process_gid_effective, selected_process_gid_saved


    # ----------------------- Get number of threads of the process -----------------------
    def process_details_process_number_of_threads_func(self, stat_output_split):

        selected_process_num_threads = stat_output_split[-33]

        return selected_process_num_threads


    # ----------------------- Get threads (TIDs) of the process -----------------------
    def process_details_process_tids_func(self, task_ls_output):

        task_ls_output_lines = task_ls_output.split("\n")
        selected_process_threads = [filename for filename in task_ls_output_lines if filename.isdigit()]
        selected_process_threads = sorted(selected_process_threads, key=int)

        return selected_process_threads


    # ----------------------- Get the last CPU core number which process executed on -----------------------
    def process_details_process_cpu_number_func(self, stat_output_split):

        selected_process_cpu_num = stat_output_split[-14]

        return selected_process_cpu_num


    # ----------------------- Get CPU times of the process -----------------------
    def process_details_process_cpu_times_func(self, stat_output_split):

        selected_process_cpu_times_user = stat_output_split[-39]
        selected_process_cpu_times_kernel = stat_output_split[-38]
        selected_process_cpu_times_children_user = stat_output_split[-37]
        selected_process_cpu_times_children_kernel = stat_output_split[-36]
        selected_process_cpu_times_io_wait = stat_output_split[-11]

        return selected_process_cpu_times_user, selected_process_cpu_times_kernel, selected_process_cpu_times_children_user, selected_process_cpu_times_children_kernel, selected_process_cpu_times_io_wait


    # ----------------------- Get process context switches -----------------------
    def process_details_process_context_switches_func(self, status_output_split):

        for line in status_output_split:
            if line.startswith("voluntary_ctxt_switches:"):
                selected_process_num_ctx_switches_voluntary = line.split(":")[1].strip()
            if line.startswith("nonvoluntary_ctxt_switches:"):
                selected_process_num_ctx_switches_nonvoluntary = line.split(":")[1].strip()

        return selected_process_num_ctx_switches_voluntary, selected_process_num_ctx_switches_nonvoluntary


    # ----------------------- Get process memory (VMS) -----------------------
    def process_details_process_memory_vms_func(self, stat_output_split):

        selected_process_memory_vms = int(stat_output_split[-30])

        return selected_process_memory_vms


    # ----------------------- Get process memory (Shared) -----------------------
    def process_details_process_memory_shared_func(self, statm_output):

        selected_process_memory_shared = int(statm_output.split()[2]) * Processes.memory_page_size

        return selected_process_memory_shared


    # ----------------------- Get process memory (USS - Unique Set Size) and swap memory -----------------------
    def process_details_process_memory_uss_and_swap_func(self, smaps_output):

        smaps_output_lines = smaps_output.split("\n")

        private_clean = 0
        private_dirty = 0
        memory_swap = 0
        for line in smaps_output_lines:
            if "Private_Clean:" in line:
                private_clean = private_clean + int(line.split(":")[1].split()[0].strip())
            if "Private_Dirty:" in line:
                private_dirty = private_dirty + int(line.split(":")[1].split()[0].strip())
            if line.startswith("Swap:"):
                memory_swap = memory_swap + int(line.split(":")[1].split()[0].strip())
        # Kilobytes value converted into bytes value (there is a negligible deviation in bytes unit)
        selected_process_memory_uss = (private_clean + private_dirty) * 1024
        selected_process_memory_swap = memory_swap * 1024

        return selected_process_memory_uss, selected_process_memory_swap


    # ----------------------- Get process read count, write count -----------------------
    def process_details_process_read_write_counts_func(self, io_output_lines):

        if io_output_lines != ["-"]:
            selected_process_read_count = int(io_output_lines[2].split(":")[1])
            selected_process_write_count = int(io_output_lines[3].split(":")[1])
        # Root access is needed for reading "/proc/[PID]/io" file else it gives error.
        else:
            selected_process_read_count = 0
            selected_process_write_count = 0

        return selected_process_read_count, selected_process_write_count


    # ----------------------- Get process cmdline -----------------------
    def process_details_process_cmdline_func(self, cmdline_output):

        selected_process_cmdline = cmdline_output.split(" ")

        if selected_process_cmdline == [""]:
            selected_process_cmdline = "-"

        return selected_process_cmdline


    # ----------------------- Get process cwd and open files -----------------------
    def process_details_process_exe_cwd_open_files_func(self, selected_process_pid, fd_ls_output):

        command_list = ["readlink"]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list

        # "/proc/self" folder will be used for splitting the "readlink" command output.
        command_list.append("/proc/self")

        # Get process exe path.
        selected_process_exe_path = "/proc/" + selected_process_pid + "/exe"
        command_list.append(selected_process_exe_path)

        # Append command for splitting command output.
        command_list.append("/proc/self")

        # Get process cwd path.
        selected_process_cwd_path = "/proc/" + selected_process_pid + "/cwd"
        command_list.append(selected_process_cwd_path)

        # Append command for splitting command output.
        command_list.append("/proc/self")

        # Get process fd path list.
        fd_ls_output_lines = fd_ls_output.split("\n")
        selected_process_fds = [filename for filename in fd_ls_output_lines if filename.isdigit()]
        selected_process_fds = sorted(selected_process_fds, key=int)

        selected_process_fd_paths = []
        for fd in selected_process_fds:
            selected_process_fd_paths.append("/proc/" + selected_process_pid + "/fd/" + fd)

        if selected_process_fd_paths == []:
            selected_process_fd_paths = "-"

        # Append command list for process open files.
        if selected_process_fd_paths != "-":
            for path in selected_process_fd_paths:
                command_list.append(path)

        # Get "readlink" command output.
        readlink_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE)).stdout.decode().strip()
        readlink_output_lines = readlink_output.split("\n")

        # Split the "readlink" command output.
        split_text = readlink_output_lines[0].strip()
        readlink_output_split = readlink_output.split(split_text)
        del readlink_output_split[0]

        # Get process exe.
        selected_process_exe = readlink_output_split[0].strip()
        if selected_process_exe == "":
            selected_process_exe = "-"

        # Get process cwd.
        selected_process_cwd = readlink_output_split[1].strip()
        if selected_process_cwd == "":
            selected_process_cwd = "-"

        # Get process open files list.
        selected_process_open_files = []
        readlink_output_split = readlink_output_split[2].strip().split("\n")
        for file in readlink_output_split:
            file_strip = file.strip()
            # Prevent adding lines which are not files.
            if file_strip.count("/") > 1:
                selected_process_open_files.append(file_strip)

        if selected_process_open_files == []:
            selected_process_open_files = "-"

        return selected_process_exe, selected_process_cwd, selected_process_open_files


# Generate object for every process because more than one process window can be opened on Processes tab.
processes_details_object_list = []
def processes_details_show_process_details():

    # Prevent opening more than 8 windows in order to avoid very high CPU usage.
    # This limit is 3 for Flatpak environment. Because CPU usage is higher in this environment.
    if Config.environment_type == "flatpak":
        max_number_of_windows = 3
    else:
        max_number_of_windows = 8

    if len(processes_details_object_list) == max_number_of_windows:
        return

    processes_details_object_list.append(ProcessesDetails(Processes.selected_process_pid))
    processes_details_object_list[-1].window2101w.show()

