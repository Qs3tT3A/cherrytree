# -*- coding: UTF-8 -*-
#
#       config.py
#
#       Copyright 2009-2011 Giuseppe Penone <giuspen@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os, sys, xml.dom.minidom, gtk, pango, subprocess, base64
import cons

ICONS_SIZE = {1: gtk.ICON_SIZE_MENU, 2: gtk.ICON_SIZE_SMALL_TOOLBAR, 3: gtk.ICON_SIZE_LARGE_TOOLBAR,
              4: gtk.ICON_SIZE_DND, 5: gtk.ICON_SIZE_DIALOG}


def config_file_load(inst):
    """Load the Preferences from Config File"""
    if os.path.isfile(cons.CONFIG_PATH):
        config_file_descriptor = file(cons.CONFIG_PATH, 'r')
        config_str = config_file_descriptor.read()
        config_file_descriptor.close()
        dom = xml.dom.minidom.parseString(config_str)
        dom_iter = dom.firstChild
        if dom_iter.nodeName != "config":
            print "invalid config file!"
            return
        if dom_iter.hasAttribute("win_is_maximized"):
            inst.win_is_maximized = (dom_iter.attributes["win_is_maximized"].value == "True")
        else: inst.win_is_maximized = False
        # restore window size and position
        if inst.win_is_maximized: inst.window.maximize()
        else:
            if dom_iter.hasAttribute("win_size_w") and dom_iter.hasAttribute("win_size_h"):
                win_size = [int(dom_iter.attributes["win_size_w"].value),
                            int(dom_iter.attributes["win_size_h"].value)]
                inst.window.resize(win_size[0], win_size[1])
            if dom_iter.hasAttribute("win_position_x") and dom_iter.hasAttribute("win_position_y"):
                win_position = [int(dom_iter.attributes["win_position_x"].value),
                                int(dom_iter.attributes["win_position_y"].value)]
                inst.window.move(win_position[0], win_position[1])
        if dom_iter.hasAttribute("toolbar_visible") and dom_iter.attributes["toolbar_visible"].value == "False":
            inst.toolbar_visible = False
        else: inst.toolbar_visible = True
        if dom_iter.hasAttribute("file_dir"): inst.file_dir = dom_iter.attributes["file_dir"].value
        else: inst.file_dir = ""
        if dom_iter.hasAttribute("file_name"): inst.file_name = dom_iter.attributes["file_name"].value
        else: inst.file_name = ""
        if dom_iter.hasAttribute("node_path"):
            # restor the selected node
            str_path_list_of_str = dom_iter.attributes["node_path"].value
            path_list_of_str = str_path_list_of_str.split()
            path_list_of_int = []
            for element in path_list_of_str: path_list_of_int.append( int(element) )
            inst.node_path = tuple(path_list_of_int)
            if dom_iter.hasAttribute("cursor_position"):
                inst.cursor_position = int( dom_iter.attributes["cursor_position"].value )
        else: inst.node_path = None
        if dom_iter.hasAttribute("hpaned_pos"):
            inst.hpaned_pos = int( dom_iter.attributes["hpaned_pos"].value )
        else: inst.hpaned_pos = 170
        if dom_iter.hasAttribute("text_font"): inst.text_font = dom_iter.attributes["text_font"].value
        else: inst.text_font = "Sans 9" # default text font
        if dom_iter.hasAttribute("tree_font"): inst.tree_font = dom_iter.attributes["tree_font"].value
        else: inst.tree_font = "Sans 8" # default tree font
        if dom_iter.hasAttribute("code_font"): inst.code_font = dom_iter.attributes["code_font"].value
        else: inst.code_font = "Monospace 9" # default code font
        if dom_iter.hasAttribute("show_line_numbers"):
            inst.show_line_numbers = (dom_iter.attributes["show_line_numbers"].value == "True")
        else: inst.show_line_numbers = False
        if dom_iter.hasAttribute("syntax_highlighting"):
            inst.syntax_highlighting = dom_iter.attributes["syntax_highlighting"].value
        else: inst.syntax_highlighting = cons.CUSTOM_COLORS_ID
        if dom_iter.hasAttribute("spaces_instead_tabs"):
            inst.spaces_instead_tabs = (dom_iter.attributes["spaces_instead_tabs"].value == "True")
        else: inst.spaces_instead_tabs = True
        if dom_iter.hasAttribute("tabs_width"): inst.tabs_width = int( dom_iter.attributes["tabs_width"].value )
        else: inst.tabs_width = 3
        if dom_iter.hasAttribute("line_wrapping"):
            inst.line_wrapping = (dom_iter.attributes["line_wrapping"].value == "True")
        else: inst.line_wrapping = True
        if dom_iter.hasAttribute("auto_indent"): inst.auto_indent = (dom_iter.attributes["auto_indent"].value == "True")
        else: inst.auto_indent = True
        if dom_iter.hasAttribute("systray"): inst.systray = (dom_iter.attributes["systray"].value == "True")
        else: inst.systray = False
        if dom_iter.hasAttribute("autosave") and dom_iter.hasAttribute("autosave_val"):
            inst.autosave = [(dom_iter.attributes["autosave"].value == "True"),
                             int(dom_iter.attributes["autosave_val"].value)]
        else: inst.autosave = [False, 5]
        if dom_iter.hasAttribute("expand_tree"): inst.expand_tree = (dom_iter.attributes["expand_tree"].value == "True")
        else: inst.expand_tree = False
        if dom_iter.hasAttribute("expanded_collapsed_string"):
            inst.expanded_collapsed_string = dom_iter.attributes["expanded_collapsed_string"].value
        else: inst.expanded_collapsed_string = ""
        if dom_iter.hasAttribute("pick_dir"): inst.pick_dir = dom_iter.attributes["pick_dir"].value
        else: inst.pick_dir = ""
        if dom_iter.hasAttribute("link_type"): inst.link_type = dom_iter.attributes["link_type"].value
        else: inst.link_type = "webs"
        if dom_iter.hasAttribute("show_node_name_label"):
            inst.show_node_name_label = (dom_iter.attributes["show_node_name_label"].value == "True")
        else: inst.show_node_name_label = True
        if dom_iter.hasAttribute("table_rows"):
            inst.table_rows = int(dom_iter.attributes["table_rows"].value)
        else: inst.table_rows = 3
        if dom_iter.hasAttribute("table_columns"):
            inst.table_columns = int(dom_iter.attributes["table_columns"].value)
        else: inst.table_columns = 3
        if dom_iter.hasAttribute("toolbar_icon_size"):
            inst.toolbar_icon_size = int( dom_iter.attributes["toolbar_icon_size"].value )
            if inst.toolbar_icon_size not in ICONS_SIZE: inst.toolbar_icon_size = 1
        else: inst.toolbar_icon_size = 1
        if dom_iter.hasAttribute("table_column_mode"):
            inst.table_column_mode = dom_iter.attributes["table_column_mode"].value
        else: inst.table_column_mode = "rename"
        if dom_iter.hasAttribute("table_col_min"):
            inst.table_col_min = int(dom_iter.attributes["table_col_min"].value)
        else: inst.table_col_min = 40
        if dom_iter.hasAttribute("table_col_max"):
            inst.table_col_max = int(dom_iter.attributes["table_col_max"].value)
        else: inst.table_col_max = 60
        if dom_iter.hasAttribute("cherry_wrap_width"):
            inst.cherry_wrap_width = int(dom_iter.attributes["cherry_wrap_width"].value)
        else: inst.cherry_wrap_width = 130
        if dom_iter.hasAttribute("start_on_systray"):
            inst.start_on_systray = (dom_iter.attributes["start_on_systray"].value == "True")
        else: inst.start_on_systray = False
        if dom_iter.hasAttribute("weblink_custom_action"):
            temp_str = dom_iter.attributes["weblink_custom_action"].value
            if temp_str[:4] == "True": inst.weblink_custom_action = [True, temp_str[4:]]
            else: inst.weblink_custom_action = [False, temp_str[5:]]
        else: inst.weblink_custom_action = [False, "firefox %s"]
        if dom_iter.hasAttribute("filelink_custom_action"):
            temp_str = dom_iter.attributes["filelink_custom_action"].value
            if temp_str[:4] == "True": inst.filelink_custom_action = [True, temp_str[4:]]
            else: inst.filelink_custom_action = [False, temp_str[5:]]
        else: inst.filelink_custom_action = [False, "xdg-open %s"]
        if dom_iter.hasAttribute("folderlink_custom_action"):
            temp_str = dom_iter.attributes["folderlink_custom_action"].value
            if temp_str[:4] == "True": inst.folderlink_custom_action = [True, temp_str[4:]]
            else: inst.folderlink_custom_action = [False, temp_str[5:]]
        else: inst.folderlink_custom_action = [False, "xdg-open %s"]
        if dom_iter.hasAttribute("codebox_width"):
            inst.glade.spinbutton_codebox_width.set_value(int(dom_iter.attributes["codebox_width"].value))
        else: inst.glade.spinbutton_codebox_width.set_value(700)
        if dom_iter.hasAttribute("codebox_height"):
            inst.glade.spinbutton_codebox_height.set_value(int(dom_iter.attributes["codebox_height"].value))
        else: inst.glade.spinbutton_codebox_height.set_value(100)
        if dom_iter.hasAttribute("codebox_width_pixels"):
            inst.glade.radiobutton_codebox_pixels.set_active(dom_iter.attributes["codebox_width_pixels"].value == "True")
            inst.glade.radiobutton_codebox_percent.set_active(dom_iter.attributes["codebox_width_pixels"].value != "True")
        if dom_iter.hasAttribute("check_version"):
            inst.check_version = (dom_iter.attributes["check_version"].value == "True")
        else: inst.check_version = False
        if dom_iter.hasAttribute("backup_copy"):
            inst.backup_copy = (dom_iter.attributes["backup_copy"].value == "True")
        else: inst.backup_copy = True
        if dom_iter.hasAttribute("autosave_on_quit"):
            inst.autosave_on_quit = (dom_iter.attributes["autosave_on_quit"].value == "True")
        else: inst.autosave_on_quit = False
        if dom_iter.hasAttribute("tree_right_side"):
            inst.tree_right_side = (dom_iter.attributes["tree_right_side"].value == "True")
        else: inst.tree_right_side = False
        if dom_iter.hasAttribute("nodes_icons"):
            inst.nodes_icons = dom_iter.attributes["nodes_icons"].value
        else: inst.nodes_icons = "c"
        inst.recent_docs = []
        if dom_iter.hasAttribute("recent_docs"):
            temp_recent_docs = dom_iter.attributes["recent_docs"].value.split(cons.CHAR_SPACE)
            for element in temp_recent_docs:
                if element: inst.recent_docs.append(base64.b64decode(element))
    else:
        if sys.platform[0:3] != "win": subprocess.call(cons.SHOW_MENU_ICONS, shell=True)
        inst.file_dir = ""
        inst.file_name = ""
        inst.node_path = None
        inst.tree_font = "Sans 8" # default tree font
        inst.text_font = "Sans 9" # default text font
        inst.code_font = "Monospace 9" # default code font
        inst.show_line_numbers = False
        inst.syntax_highlighting = cons.CUSTOM_COLORS_ID
        inst.spaces_instead_tabs = True
        inst.tabs_width = 3
        inst.line_wrapping = True
        inst.auto_indent = True
        inst.systray = False
        inst.autosave = [False, 5]
        inst.win_is_maximized = False
        inst.expand_tree = False
        inst.expanded_collapsed_string = ""
        inst.pick_dir = ""
        inst.link_type = "webs"
        inst.toolbar_icon_size = 1
        inst.table_rows = 3
        inst.table_columns = 3
        inst.table_column_mode = "rename"
        inst.table_col_min = 40
        inst.table_col_max = 60
        inst.cherry_wrap_width = 130
        inst.start_on_systray = False
        inst.weblink_custom_action = [False, "firefox %s"]
        inst.filelink_custom_action = [False, "xdg-open %s"]
        inst.folderlink_custom_action = [False, "xdg-open %s"]
        inst.glade.spinbutton_codebox_width.set_value(700)
        inst.glade.spinbutton_codebox_height.set_value(100)
        inst.check_version = False
        inst.backup_copy = True
        inst.autosave_on_quit = False
        inst.tree_right_side = False
        inst.hpaned_pos = 170
        inst.show_node_name_label = True
        inst.nodes_icons = "c"
        inst.recent_docs = []
        inst.toolbar_visible = True

def config_file_apply(inst):
    """Apply the Preferences from Config File"""
    inst.user_active = False
    # treeview
    inst.hpaned.set_property('position', inst.hpaned_pos)
    inst.header_node_name_label.set_property("visible", inst.show_node_name_label)
    inst.set_treeview_font()
    inst.glade.fontbutton_tree.set_font_name(inst.tree_font)
    # sourceview
    inst.glade.fontbutton_text.set_font_name(inst.text_font)
    inst.glade.fontbutton_code.set_font_name(inst.code_font)
    inst.sourceview.set_show_line_numbers(inst.show_line_numbers)
    inst.glade.checkbutton_line_nums.set_active(inst.show_line_numbers)
    inst.sourceview.set_insert_spaces_instead_of_tabs(inst.spaces_instead_tabs)
    inst.glade.checkbutton_spaces_tabs.set_active(inst.spaces_instead_tabs)
    inst.sourceview.set_tab_width(inst.tabs_width)
    inst.glade.spinbutton_tab_width.set_value(inst.tabs_width)
    if inst.line_wrapping: inst.sourceview.set_wrap_mode(gtk.WRAP_WORD)
    else: inst.sourceview.set_wrap_mode(gtk.WRAP_NONE)
    inst.glade.checkbutton_line_wrap.set_active(inst.line_wrapping)
    inst.sourceview.set_auto_indent(inst.auto_indent)
    inst.glade.checkbutton_auto_indent.set_active(inst.auto_indent)
    inst.glade.checkbutton_systray.set_active(inst.systray)
    inst.glade.spinbutton_autosave.set_value(inst.autosave[1])
    inst.glade.spinbutton_autosave.set_sensitive(inst.autosave[0])
    inst.glade.checkbutton_autosave.set_active(inst.autosave[0])
    inst.glade.checkbutton_expand_tree.set_active(inst.expand_tree)
    inst.glade.checkbutton_newer_version.set_active(inst.check_version)
    inst.glade.checkbutton_backup_before_saving.set_active(inst.backup_copy)
    inst.glade.checkbutton_autosave_on_quit.set_active(inst.autosave_on_quit)
    inst.glade.checkbutton_tree_right_side.set_active(inst.tree_right_side)
    inst.glade.checkbutton_start_on_systray.set_active(inst.start_on_systray)
    inst.glade.checkbutton_start_on_systray.set_sensitive(inst.systray)
    # custom link clicked actions
    inst.glade.checkbutton_custom_weblink_cmd.set_active(inst.weblink_custom_action[0])
    inst.glade.entry_custom_weblink_cmd.set_sensitive(inst.weblink_custom_action[0])
    inst.glade.entry_custom_weblink_cmd.set_text(inst.weblink_custom_action[1])
    inst.glade.checkbutton_custom_filelink_cmd.set_active(inst.filelink_custom_action[0])
    inst.glade.entry_custom_filelink_cmd.set_sensitive(inst.filelink_custom_action[0])
    inst.glade.entry_custom_filelink_cmd.set_text(inst.filelink_custom_action[1])
    inst.glade.checkbutton_custom_folderlink_cmd.set_active(inst.folderlink_custom_action[0])
    inst.glade.entry_custom_folderlink_cmd.set_sensitive(inst.folderlink_custom_action[0])
    inst.glade.entry_custom_folderlink_cmd.set_text(inst.folderlink_custom_action[1])
    #
    inst.glade.radiobutton_link_website.set_active(inst.link_type == "webs")
    inst.glade.radiobutton_link_node_anchor.set_active(inst.link_type == "node")
    inst.glade.radiobutton_link_file.set_active(inst.link_type == "file")
    inst.glade.table_column_rename_radiobutton.set_active(inst.table_column_mode == "rename")
    inst.glade.table_column_delete_radiobutton.set_active(inst.table_column_mode == "delete")
    inst.glade.table_column_add_radiobutton.set_active(inst.table_column_mode == "add")
    inst.glade.table_column_left_radiobutton.set_active(inst.table_column_mode == "left")
    inst.glade.table_column_right_radiobutton.set_active(inst.table_column_mode == "right")
    inst.glade.radiobutton_node_icon_cherry.set_active(inst.nodes_icons == "c")
    inst.glade.radiobutton_node_icon_bullet.set_active(inst.nodes_icons == "b")
    inst.glade.radiobutton_node_icon_none.set_active(inst.nodes_icons == "n")
    inst.glade.spinbutton_table_rows.set_value(inst.table_rows)
    inst.glade.spinbutton_table_columns.set_value(inst.table_columns)
    inst.glade.spinbutton_table_col_min.set_value(inst.table_col_min)
    inst.glade.spinbutton_table_col_max.set_value(inst.table_col_max)
    inst.glade.spinbutton_tree_nodes_names_width.set_value(inst.cherry_wrap_width)
    inst.renderer_text.set_property('wrap-width', inst.cherry_wrap_width)
    inst.ui.get_widget("/ToolBar").set_property("visible", inst.toolbar_visible)
    inst.ui.get_widget("/ToolBar").set_style(gtk.TOOLBAR_ICONS)
    inst.ui.get_widget("/ToolBar").set_property("icon-size", ICONS_SIZE[inst.toolbar_icon_size])
    if inst.autosave[0]: inst.autosave_timer_start()
    inst.user_active = True

def config_file_save(inst):
    """Save the Preferences to Config File"""
    dom = xml.dom.minidom.Document()
    config = dom.createElement("config")
    config.setAttribute("toolbar_visible", str( inst.ui.get_widget("/ToolBar").get_property('visible') ) )
    config.setAttribute("file_dir", inst.file_dir)
    config.setAttribute("file_name", inst.file_name)
    config.setAttribute("win_is_maximized", str(inst.win_is_maximized) )
    if not inst.win_is_maximized:
        win_position = inst.window.get_position()
        win_size = inst.window.get_size()
        config.setAttribute("win_position_x", str(win_position[0]) )
        config.setAttribute("win_position_y", str(win_position[1]) )
        config.setAttribute("win_size_w", str(win_size[0]) )
        config.setAttribute("win_size_h", str(win_size[1]) )
    config.setAttribute("hpaned_pos", str(inst.hpaned.get_property('position')) )
    if inst.curr_tree_iter != None:
        path_list_of_str = []
        for element in inst.treestore.get_path(inst.curr_tree_iter):
            path_list_of_str.append( str(element) )
        config.setAttribute("node_path", " ".join(path_list_of_str) )
        config.setAttribute("cursor_position", str(inst.curr_buffer.get_property('cursor-position') ) )
    config.setAttribute("text_font", inst.text_font)
    config.setAttribute("tree_font", inst.tree_font)
    config.setAttribute("code_font", inst.code_font)
    config.setAttribute("show_line_numbers", str(inst.show_line_numbers) )
    config.setAttribute("syntax_highlighting", inst.syntax_highlighting)
    config.setAttribute("spaces_instead_tabs", str(inst.spaces_instead_tabs) )
    config.setAttribute("tabs_width", str(inst.tabs_width) )
    config.setAttribute("line_wrapping", str(inst.line_wrapping) )
    config.setAttribute("auto_indent", str(inst.auto_indent) )
    config.setAttribute("systray", str(inst.systray) )
    config.setAttribute("autosave", str(inst.autosave[0]) )
    config.setAttribute("autosave_val", str(inst.autosave[1]) )
    config.setAttribute("pick_dir", inst.pick_dir)
    config.setAttribute("link_type", inst.link_type)
    config.setAttribute("show_node_name_label", str(inst.header_node_name_label.get_property("visible") ) )
    config.setAttribute("toolbar_icon_size", str(inst.toolbar_icon_size) )
    config.setAttribute("table_rows", str(inst.table_rows) )
    config.setAttribute("table_columns", str(inst.table_columns) )
    config.setAttribute("table_column_mode", inst.table_column_mode)
    config.setAttribute("table_col_min", str(inst.table_col_min))
    config.setAttribute("table_col_max", str(inst.table_col_max))
    config.setAttribute("cherry_wrap_width", str(inst.cherry_wrap_width))
    config.setAttribute("start_on_systray", str(inst.start_on_systray))
    config.setAttribute("weblink_custom_action", str(inst.weblink_custom_action[0])+inst.weblink_custom_action[1])
    config.setAttribute("filelink_custom_action", str(inst.filelink_custom_action[0])+inst.filelink_custom_action[1])
    config.setAttribute("folderlink_custom_action", str(inst.folderlink_custom_action[0])+inst.folderlink_custom_action[1])
    config.setAttribute("expand_tree", str(inst.expand_tree) )
    if not inst.expand_tree:
        get_tree_expanded_collapsed_string(inst)
        config.setAttribute("expanded_collapsed_string", inst.expanded_collapsed_string)
    config.setAttribute("codebox_width", str(int(inst.glade.spinbutton_codebox_width.get_value())))
    config.setAttribute("codebox_height", str(int(inst.glade.spinbutton_codebox_height.get_value())))
    config.setAttribute("codebox_width_pixels", str(inst.glade.radiobutton_codebox_pixels.get_active()))
    config.setAttribute("check_version", str(inst.check_version))
    config.setAttribute("backup_copy", str(inst.backup_copy))
    config.setAttribute("autosave_on_quit", str(inst.autosave_on_quit))
    config.setAttribute("tree_right_side", str(inst.tree_right_side))
    config.setAttribute("nodes_icons", inst.nodes_icons)
    if inst.recent_docs:
        temp_recent_docs = []
        for element in inst.recent_docs:
            temp_recent_docs.append(base64.b64encode(element))
        str_recent_docs = cons.CHAR_SPACE.join(temp_recent_docs)
    else: str_recent_docs = ""
    config.setAttribute("recent_docs", str_recent_docs)
    dom.appendChild(config)
    string_text = dom.toxml()
    config_file_descriptor = file(cons.CONFIG_PATH, 'w')
    config_file_descriptor.write(string_text)
    config_file_descriptor.close()

def get_tree_expanded_collapsed_string(inst):
    """Returns a String Containing the Info about Expanded and Collapsed Nodes"""
    expanded_collapsed_string = ""
    tree_iter = inst.treestore.get_iter_first()
    while tree_iter != None:
        expanded_collapsed_string += get_tree_expanded_collapsed_string_iter(tree_iter, inst)
        tree_iter = inst.treestore.iter_next(tree_iter)
    if len(expanded_collapsed_string) > 0: inst.expanded_collapsed_string = expanded_collapsed_string[1:]
    else: inst.expanded_collapsed_string = ""

def get_tree_expanded_collapsed_string_iter(tree_iter, inst):
    """Iter of the Info about Expanded and Collapsed Nodes"""
    expanded_collapsed_string = "_%s,%s" % (inst.treestore[tree_iter][3],
                                            inst.treeview.row_expanded(inst.treestore.get_path(tree_iter)))
    tree_iter = inst.treestore.iter_children(tree_iter)
    while tree_iter != None:
        expanded_collapsed_string += get_tree_expanded_collapsed_string_iter(tree_iter, inst)
        tree_iter = inst.treestore.iter_next(tree_iter)
    return expanded_collapsed_string

def set_tree_expanded_collapsed_string(inst):
    """Parses the String Containing the Info about Expanded and Collapsed Nodes"""
    inst.treeview.collapse_all()
    if inst.expanded_collapsed_string == "": return
    expanded_collapsed_dict = {}
    expanded_collapsed_vector = inst.expanded_collapsed_string.split('_')
    for element in expanded_collapsed_vector:
        couple = element.split(',')
        expanded_collapsed_dict[couple[0]] = couple[1]
    tree_iter = inst.treestore.get_iter_first()
    while tree_iter != None:
        set_tree_expanded_collapsed_string_iter(tree_iter, expanded_collapsed_dict, inst)
        tree_iter = inst.treestore.iter_next(tree_iter)

def set_tree_expanded_collapsed_string_iter(tree_iter, expanded_collapsed_dict, inst):
    """Iter of the Expanded and Collapsed Nodes Parsing"""
    node_id = str(inst.treestore[tree_iter][3])
    if node_id in expanded_collapsed_dict and expanded_collapsed_dict[node_id] == "True":
        inst.treeview.expand_row(inst.treestore.get_path(tree_iter), open_all=False)
    tree_iter = inst.treestore.iter_children(tree_iter)
    while tree_iter != None:
        set_tree_expanded_collapsed_string_iter(tree_iter, expanded_collapsed_dict, inst)
        tree_iter = inst.treestore.iter_next(tree_iter)