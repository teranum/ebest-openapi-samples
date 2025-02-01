import aiohttp, asyncio, base64, json, os, sys, types, uuid, webbrowser
from datetime import datetime
from glob import glob
from cryptography.fernet import Fernet

# PySide6로 변경시 PyQt6를 PySide6로 변경
from PyQt6 import QtGui
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import(
    QApplication, QDialog, QFormLayout, QInputDialog, QLabel, QLineEdit, QMainWindow, QMenu, QPushButton,
    QPlainTextEdit, QCheckBox, QListWidget, QSpacerItem, QSplitter, QHBoxLayout, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QListWidgetItem
    )

import syntax
from qasync import QEventLoop, asyncSlot
from ebest import OpenApi
from common import set_ext_func, print as custom_print
from prettytable import PrettyTable

class LOG_TYPE:
    LOG:int = 0
    MESSAGE:int = 1
    REALTIME:int = 2

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        set_ext_func(self.appent_result_line, self.get_input_text)

        # const
        self.mac_address = f'{uuid.getnode():x}'.upper()
        self.profile_count = 8
        self.cipher_suite = Fernet(base64.urlsafe_b64encode((self.mac_address+self.mac_address+self.mac_address).encode().ljust(32)[:32]))
        self.sample_filter = "/??.*.py"

        # setting backup folder
        self.backup_folder = os.path.dirname(os.path.abspath(__file__)) + "\\Backup_devcenter"
        if not os.path.exists(self.backup_folder):
            os.makedirs(self.backup_folder)

        # loading initial setting data
        settiong_file_path = self.backup_folder + "\\setting.json"
        self.settings = dict()
        if os.path.exists(settiong_file_path):
            try:
                with open(settiong_file_path, "r", encoding='utf8') as f:
                    self.settings = json.load(f)
                    f.close()
            except :
                pass

        self.initUI()

        # rersource
        self.root_groups = list[RootGroup]()
        self.map_trprops = dict()

        # OpenApi
        self.api = OpenApi()

        # connect event
        self.api.on_message.connect(lambda api, msg: self.output_log(LOG_TYPE.MESSAGE, msg))
        self.api.on_realtime.connect(lambda api, code, key, datas: self.output_log(LOG_TYPE.REALTIME, f'{code}, {key}, {datas}'))

        # other variables
        self.cur_tr_prop = None
        self.cur_sample = str()

        self.output_log(LOG_TYPE.LOG, "시작")

    def initUI(self):
        '''UI 초기화'''
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # check dark mode
        is_darkMode = QtGui.QPalette().color(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText).lightness() > 128

        #region UI design
        self.setWindowTitle("LS-OpenApi-DevCenter")
        self.setFont(QtGui.QFont("굴림체", 9))

        window_width = self.settings.get("window_width")
        if window_width is None or window_width < 300:
            window_width = 1450
        window_height = self.settings.get("window_height")
        if window_height is None or window_height < 300:
            window_height = 960

        self.resize(window_width, window_height)

        # 메뉴(File, Tool, Help)
        menu_file = self.menuBar().addMenu(self.tr("&File"))
        self.login_menu = menu_file.addMenu("Login")
        self.menu_profiles = list[QMenu]()
        profile_names = [None] * self.profile_count
        for i in range(self.profile_count):
            def_key = f"Profile {i+1}"
            profile_obj = self.settings.get(def_key)
            if profile_obj is None:
                profile_obj = {"name": def_key, "remember": False, "appkey": "", "appsecretkey": ""}
                self.settings[def_key] = profile_obj
            profile_names[i] = profile_obj.get('name')
            if profile_names[i] is None:
                profile_names[i] = def_key
            profile_login = self.login_menu.addAction(profile_names[i])
            profile_login.triggered.connect(lambda checked, i=i: self.func_profile_login(i))
            self.menu_profiles.append(profile_login)

        menu_macaddress = menu_file.addAction("MacAddress")
        menu_macaddress.triggered.connect(self.set_macaddress)
        menu_logout = menu_file.addAction("Logout")
        menu_logout.triggered.connect(self.func_logout)
        menu_file.addSeparator()
        quit_act = menu_file.addAction(self.tr("E&xit"))
        quit_act.triggered.connect(self.close)

        menu_tool = self.menuBar().addMenu(self.tr("&Tool"))
        tool_action_names = ["전체 URL", "TR필드"]
        tool_action_count = len(tool_action_names)
        for i in range(tool_action_count):
            action = menu_tool.addAction(tool_action_names[i])
            action.triggered.connect(lambda checked, i=i: self.tool_action(tool_action_names[i]))

        menu_help = self.menuBar().addMenu(self.tr("&Help"))
        open_homepage = menu_help.addAction("LS증권 OpenApi 홈페이지")
        open_homepage.triggered.connect(lambda: webbrowser.open_new_tab("https://openapi.ls-sec.co.kr/intro"))

        # 위젯
        self.text_search = QLineEdit()
        self.btn_search = QPushButton("검색", self)
        layout_search = QHBoxLayout()
        layout_search.addWidget(self.text_search)
        layout_search.addWidget(self.btn_search)

        self.tree_tr_list = QTreeWidget(self)
        self.tree_tr_list.setHeaderLabels(["tr코드", "tr명"])
        self.tree_tr_list.header().resizeSection(0, 180)

        self.tree_sample_list = QTreeWidget(self)
        self.tree_sample_list.setHeaderLabels(["샘플코드"])
        sum_samples_list = 0

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.sample_dir = cur_dir
        for file in glob(self.sample_dir + self.sample_filter):
            QTreeWidgetItem(self.tree_sample_list, [os.path.basename(file)])
            sum_samples_list += 1

        self.tab_code_list = QTabWidget(self)
        self.tab_code_list.addTab(self.tree_tr_list, "Tr목록")
        self.tab_code_list.addTab(self.tree_sample_list, f"샘플목록 ({sum_samples_list})")
        self.tab_code_list.setTabPosition(QTabWidget.TabPosition.South)
        if is_darkMode:
            self.tab_code_list.setStyleSheet("QTabBar::tab {color: gray;} QTabBar::tab:selected {color: white;}")
        else:
            self.tab_code_list.setStyleSheet("QTabBar::tab {color: gray;} QTabBar::tab:selected {color: black;}")
        self.tab_code_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tab_code_list.customContextMenuRequested.connect(self.on_tree_context_menu)

        layout_left = QVBoxLayout()
        layout_left.setContentsMargins(0, 0, 0, 0)
        layout_left.setSpacing(5);
        layout_left.addLayout(layout_search)
        layout_left.addWidget(self.tab_code_list)
        widget_left = QWidget()
        widget_left.setLayout(layout_left)

        self.doc_desc = QLineEdit()
        self.doc_desc.setReadOnly(True)
        self.btn_run = QPushButton("코드실행", self)
        self.check_clear_flag =QCheckBox("지우기", self)
        self.check_clear_flag.setChecked(True)
        self.check_show_res_flag =QCheckBox("RES보기", self)

        layout_h1 = QHBoxLayout()
        layout_h1.addWidget(self.doc_desc, 1)
        layout_h1.addWidget(self.btn_run, 0)
        layout_h1.addWidget(self.check_clear_flag, 0)
        layout_h1.addWidget(self.check_show_res_flag, 0)

        self.text_source = QPlainTextEdit()
        self.text_source.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.text_source.setTabStopDistance(
            QtGui.QFontMetricsF(self.text_source.font()).horizontalAdvance(' ') * 4)
        self.highlight = syntax.PythonHighlighter(self.text_source.document())

        save_shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+S"), self.text_source)
        save_shortcut.activated.connect(self.on_key_CTRL_S)

        layout_right = QVBoxLayout()
        layout_right.setContentsMargins(0, 0, 0, 0)
        layout_right.setSpacing(5);
        layout_right.addLayout(layout_h1)
        layout_right.addWidget(self.text_source)

        widget_desc_src = QWidget()
        widget_desc_src.setLayout(layout_right)

        self.text_result = QPlainTextEdit()
        self.text_result.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.text_result.setTabStopDistance(
            QtGui.QFontMetricsF(self.text_result.font()).horizontalAdvance(' ') * 4)

        self.tab_log_list = QTabWidget(self)
        self.list_log = QListWidget(self)
        self.list_event_message = QListWidget(self)
        self.list_event_realtime = QListWidget(self)

        self.tab_log_list.addTab(self.list_log, "로그")
        self.tab_log_list.addTab(self.list_event_message, "on_message")
        self.tab_log_list.addTab(self.list_event_realtime, "on_realtime")
        self.tab_log_list.setTabPosition(QTabWidget.TabPosition.South)
        if is_darkMode:
            self.tab_log_list.setStyleSheet("QTabBar::tab {color: gray;} QTabBar::tab:selected {color: white;}")
        else:
            self.tab_log_list.setStyleSheet("QTabBar::tab {color: gray;} QTabBar::tab:selected {color: black;}")
        self.tab_log_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tab_log_list.customContextMenuRequested.connect(self.on_log_context_menu)

        # test-bed
        label_test_bed = QLabel("테스트베드")
        label_test_bed.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_test_path = QLineEdit()
        self.text_test_in_tr_cd = QLineEdit()
        self.text_test_in_tr_cont_yn = QLineEdit()
        self.text_test_in_tr_cont_key = QLineEdit()
        self.check_test_in_wrapping = QCheckBox("wrapping", self)
        self.check_test_in_wrapping.setChecked(True)
        self.btn_test_request = QPushButton("전문요청", self)
        self.text_test_request = QPlainTextEdit()
        self.check_test_in_wrapping.checkStateChanged.connect(lambda state: self.text_test_request.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth if state == Qt.CheckState.Checked else QPlainTextEdit.LineWrapMode.NoWrap))

        layout_test_in_request = QHBoxLayout()
        layout_test_in_request.addWidget(self.check_test_in_wrapping, 0)
        layout_test_in_request.addWidget(self.btn_test_request, 0)
        layout_test_in_request.addStretch(1)
        formlayout_test_request_settings = QFormLayout()
        formlayout_test_request_settings.addRow("path", self.text_test_path)
        formlayout_test_request_settings.addRow("tr_cd", self.text_test_in_tr_cd)
        formlayout_test_request_settings.addRow("tr_cont_yn", self.text_test_in_tr_cont_yn)
        formlayout_test_request_settings.addRow("tr_cont_key", self.text_test_in_tr_cont_key)
        formlayout_test_request_settings.addRow("Request", layout_test_in_request)

        self.text_test_request_time = QLabel()
        self.text_test_request_time.setText("요청시간: ")
        self.text_test_response_time = QLabel()
        self.text_test_response_time.setText("응답시간(ms): ")
        layout_test_time = QHBoxLayout()
        layout_test_time.addWidget(self.text_test_request_time)
        layout_test_time.addWidget(self.text_test_response_time)

        layout_test_request = QVBoxLayout()
        layout_test_request.setContentsMargins(0, 7, 0, 0)
        layout_test_request.addWidget(label_test_bed)
        layout_test_request.addLayout(formlayout_test_request_settings)
        layout_test_request.addWidget(self.text_test_request)
        # layout_test_request.addLayout(layout_test_time)

        self.text_test_out_tr_cont_yn = QLineEdit()
        self.text_test_out_tr_cont_yn.setReadOnly(True)
        self.text_test_out_tr_cont_key = QLineEdit()
        self.text_test_out_tr_cont_key.setReadOnly(True)
        self.check_test_out_wrapping = QCheckBox("wrapping", self)
        self.check_test_out_wrapping.setChecked(True)
        self.text_test_response = QPlainTextEdit()
        self.text_test_response.setReadOnly(True)
        self.check_test_out_wrapping.checkStateChanged.connect(lambda state: self.text_test_response.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth if state == Qt.CheckState.Checked else QPlainTextEdit.LineWrapMode.NoWrap))
        formlayout_test_response_settings = QFormLayout()
        formlayout_test_response_settings.addRow("tr_cont_yn", self.text_test_out_tr_cont_yn)
        formlayout_test_response_settings.addRow("tr_cont_key", self.text_test_out_tr_cont_key)
        formlayout_test_response_settings.addRow("Response", self.check_test_out_wrapping)

        layout_test_response = QVBoxLayout()
        layout_test_response.setContentsMargins(0, 0, 0, 0)
        layout_test_response.addLayout(layout_test_time)
        layout_test_response.addLayout(formlayout_test_response_settings)
        layout_test_response.addWidget(self.text_test_response)

        # splitter
        splitter_v_testbed = QSplitter(Qt.Orientation.Vertical, self)
        widget_test_request = QWidget()
        widget_test_request.setLayout(layout_test_request)
        splitter_v_testbed.addWidget(widget_test_request)
        widget_test_response = QWidget()
        widget_test_response.setLayout(layout_test_response)
        splitter_v_testbed.addWidget(widget_test_response)
        splitter_v_testbed.setSizes([300,400])
        splitter_v_testbed.setStretchFactor(1, 1)

        splitter_v_dash = QSplitter(Qt.Orientation.Vertical, self)
        splitter_v_dash.addWidget(widget_desc_src)
        splitter_v_dash.addWidget(self.text_result)
        splitter_v_dash.setSizes([300,400])
        splitter_v_dash.setStretchFactor(1, 1)

        splitter_h_dash_testbed = QSplitter(Qt.Orientation.Horizontal, self)
        splitter_h_dash_testbed.addWidget(splitter_v_dash)
        splitter_h_dash_testbed.addWidget(splitter_v_testbed)
        splitter_h_dash_testbed.setSizes([380,400])
        splitter_h_dash_testbed.setStretchFactor(0, 1)

        splitter_v_main = QSplitter(Qt.Orientation.Vertical, self)
        splitter_v_main.addWidget(splitter_h_dash_testbed)
        splitter_v_main.addWidget(self.tab_log_list)
        splitter_v_main.setSizes([300,250])
        splitter_v_main.setStretchFactor(0, 1)

        splitter_h_main = QSplitter(Qt.Orientation.Horizontal, self)
        splitter_h_main.addWidget(widget_left)
        splitter_h_main.addWidget(splitter_v_main)
        splitter_h_main.setSizes([380,300])
        splitter_h_main.setStretchFactor(1, 1)

        # main layout setting
        self.setCentralWidget(splitter_h_main)
        self.setContentsMargins(5, 5, 5, 5)

        #endregion

        # UI connect event
        self.btn_search.clicked.connect(self.on_search)
        self.btn_run.clicked.connect(self.func_run)
        self.tree_tr_list.currentItemChanged.connect(self.tree_list_changed)
        self.tree_sample_list.currentItemChanged.connect(self.tree_list_changed)
        self.list_log.itemDoubleClicked.connect(self.on_log_double_click)
        self.btn_test_request.clicked.connect(self.func_test_request)
        #endregion

    def closeEvent(self, *args):
        '''종료시 처리'''
        # save settings
        self.settings["window_width"] = self.width()
        self.settings["window_height"] = self.height()
        settiong_file_path = self.backup_folder + "\\setting.json"
        with open(settiong_file_path, "w", encoding='utf8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=4)
            f.close()

    async def initalize_async(self):
        ''' 비동기 초기화 '''
        LSSiteHelper.initialize()
        filepath = self.backup_folder + "\\devcenter.trlist"
        root_groups = list[RootGroup]()
        site_loaded = False
        if os.path.exists(filepath):
            # 파일에서 TR리스트 읽어옴
            with open(filepath, "r", encoding='utf8') as f:
                lines = f.readlines()
                for line in lines:
                    words = line.strip().split("^")
                    if len(words) < 3:
                        continue
                    if words[0] == "0":
                        root_group = RootGroup(words[1], words[2])
                        root_groups.append(root_group)
                    elif words[0] == "1":
                        sub_group = {"id": words[1], "name": words[2], "accessUrl": words[3], "protocolType": words[4], "tr_props": list()}
                        root_group.add_sub_group(sub_group)
                    elif words[0] == "2":
                        tr_prop = {"id": words[1], "trCode": words[2], "trName": words[3], "transactionPerSec": words[4]}
                        sub_group['tr_props'].append(tr_prop)
        else:
            # 파일 없는 경우에만, 서버에서 TR리스트 가져옴 (서버부하방지)
            count = 0
            root_groups = await LSSiteHelper.GetRootGroups()
            oauth_node = next((x for x in root_groups if x.desc_name == "OAuth 인증"), None)
            if oauth_node is not None:
                root_groups.remove(oauth_node)
            count += 1
            for root_group in root_groups:
                subgroups = await LSSiteHelper.GetSubGroups(root_group.id)
                count += 1
                not_opened_groups = [x for x in subgroups if x['open'] != True]
                for not_opened_group in not_opened_groups:
                    subgroups.remove(not_opened_group)
                for subgroup in subgroups:
                    tr_props = await LSSiteHelper.GetTrProps(subgroup['id'])
                    count += 1
                    subgroup['tr_props'] = tr_props
                root_group.sub_groupList = subgroups
                site_loaded = True
            self.output_log(LOG_TYPE.LOG,f"TR데이터 초기화 완료: {count}")

        tr_count = 0
        for root_group in root_groups:
            item = QTreeWidgetItem(self.tree_tr_list, [root_group.desc_name])
            item.setExpanded(True)
            for subgroup in root_group.sub_groupList:
                sub_item = QTreeWidgetItem(item, [subgroup['name']])
                for tr_prop in subgroup['tr_props']:
                    tr_prop['.parent'] = subgroup
                    self.map_trprops[tr_prop['trCode']] = tr_prop
                    tr_cd = tr_prop['trCode'].strip()
                    tr_prop['trCode'] = tr_cd
                    QTreeWidgetItem(sub_item, [tr_cd, tr_prop['trName']])
                    tr_count += 1
        self.tab_code_list.setTabText(0, f"TR목록 ({tr_count})")

        self.root_groups = root_groups

        if site_loaded:
            # TR리스트 파일보관
            filepath = self.backup_folder + "\\devcenter.trlist"
            with open(filepath, "w", encoding='utf8') as f:
                lines = list()
                for root_group in self.root_groups:
                    lines.append(f"0^{root_group.id}^{root_group.desc_name}\n")
                    for subgroup in root_group.sub_groupList:
                        lines.append(f"1^{subgroup['id']}^{subgroup['name']}^{subgroup['accessUrl']}^{subgroup['protocolType']}\n")
                        for tr_prop in subgroup['tr_props']:
                            lines.append(f"2^{tr_prop['id']}^{tr_prop['trCode']}^{tr_prop['trName']}^{tr_prop['transactionPerSec']}\n")
                f.writelines(lines)
                f.close()
            pass

    def appent_result_line(self, text:str):
        '''텍스트 추가'''
        self.text_result.appendPlainText(str(text))

    def appent_result(self, text:str):
        '''텍스트 추가'''
        self.text_result.moveCursor(QtGui.QTextCursor.MoveOperation.End)
        self.text_result.insertPlainText(text)
        self.text_result.moveCursor(QtGui.QTextCursor.MoveOperation.End)

    async def get_input_text(self, prompt: str = "") -> str:
        self.appent_result_line(prompt)
        text, ok = await QAsyncDialog.getText(self, 'Input', prompt)
        if ok:
            self.appent_result(text)
            return text
        return ""

    def output_log(self, log_type:LOG_TYPE, text:str):
        '''로그 추가'''
        time_text = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        text = f"{time_text} : {text}"
        log_list = None
        if log_type == LOG_TYPE.LOG:
            log_list = self.list_log
        elif log_type == LOG_TYPE.MESSAGE:
            log_list = self.list_event_message
        elif log_type == LOG_TYPE.REALTIME:
            log_list = self.list_event_realtime
        if log_list is not None:
            if log_list.count() > 300: # 300개 이상이면 삭제
                log_list.clear()
            log_list.addItem(text)
            log_list.scrollToBottom()
            count = log_list.count()
            match log_type:
                case LOG_TYPE.LOG:
                    self.tab_log_list.setTabText(0, f"로그 ({count})")
                case LOG_TYPE.MESSAGE:
                    self.tab_log_list.setTabText(1, f"on_message ({count})")
                case LOG_TYPE.REALTIME:
                    self.tab_log_list.setTabText(2, f"on_realtime ({count})")
        else:
            print(text)

    def clear_log(self, log_type:LOG_TYPE):
        '''로그 지우기'''
        match log_type:
            case LOG_TYPE.LOG:
                self.list_log.clear()
                self.tab_log_list.setTabText(0, f"로그")
            case LOG_TYPE.MESSAGE:
                self.list_event_message.clear()
                self.tab_log_list.setTabText(1, f"on_message")
            case LOG_TYPE.REALTIME:
                self.list_event_realtime.clear()
                self.tab_log_list.setTabText(2, f"on_realtime")

    def on_search(self):
        '''검색'''
        text = self.text_search.text()
        if len(text) < 1:
            return
        def __IncludeText(next_item: QTreeWidgetItem, text: str):
            if next_item.text(0).find(text) >= 0 or next_item.text(1).find(text) >= 0:
                return next_item
            child_count = next_item.childCount()
            for i in range(child_count):
                next_child = next_item.child(i)
                item = __IncludeText(next_child, text)
                if item is not None:
                    return item
            return None
        cur_list: QTreeWidget = self.tab_code_list.currentWidget()
        currentItem = cur_list.currentItem()
        if currentItem is None:
            currentItem = cur_list.topLevelItem(0)
        next_item = cur_list.itemBelow(currentItem)
        while next_item is not None:
            item = __IncludeText(next_item, text)
            if item is not None:
                cur_list.setCurrentItem(item)
                return
            next_item = cur_list.itemBelow(next_item)

    def on_tree_context_menu(self, pos:QPoint):
        '''목록탭 컨텍스트 메뉴'''
        tree_index = self.tab_code_list.currentIndex()
        if tree_index == 1:
            def query(args):
                '''목록조회'''
                sum_samples_list = 0
                self.tree_sample_list.clear()
                for file in glob(self.sample_dir + self.sample_filter):
                    QTreeWidgetItem(self.tree_sample_list, [os.path.basename(file)])
                    sum_samples_list += 1
                    self.tab_code_list.setTabText(1, f"샘플목록 ({sum_samples_list})")

            menu = QMenu(self)
            query_action = menu.addAction("목록조회")
            query_action.triggered.connect(query)
            menu.exec(self.tab_code_list.mapToGlobal(pos))

    def tree_list_changed(self, current:QTreeWidgetItem, prev:QTreeWidgetItem):
        '''트리 선택 변경'''
        if current is not None and current.childCount() == 0:
            self.cur_sample = ""
            if self.tab_code_list.currentIndex() == 1:
                self.cur_sample = current.text(0)
                self.cur_tr_prop = None
                self.doc_desc.setText(self.cur_sample)
                self.load_sample_file(self.sample_dir + f"\\{self.cur_sample}")
            else:
                asyncio.ensure_future(self.set_code(current.text(0)))

    def on_log_context_menu(self, pos:QPoint):
        '''로그탭 컨텍스트 메뉴'''
        list_index = self.tab_log_list.currentIndex()
        list_widget = self.tab_log_list.currentWidget()
        menu = QMenu(self)
        clear_action = menu.addAction("지우기")
        clear_action.triggered.connect(lambda: self.clear_log(list_index))
        copy_action = menu.addAction("복사")
        copy_action.triggered.connect(lambda: QApplication.clipboard().setText("\n".join([list_widget.item(i).text() for i in range( list_widget.count())]) + "\n"))
        if list_index == 2:
            stop_all_realtime_action = menu.addAction("실시간 중지")
            stop_all_realtime_action.triggered.connect(self.func_remove_realtime)
        menu.exec(self.tab_log_list.mapToGlobal(pos))

    def on_key_CTRL_S(self):
        ''' 샘플 저장 '''
        if self.tab_code_list.currentIndex() == 1:
            tree_widget = self.tab_code_list.currentWidget()
            cur_item = tree_widget.currentItem()
            if cur_item is not None:
                cur_name = tree_widget.currentItem().text(0)
                file_path = self.sample_dir + f"\\{cur_name}"
                self.save_sample_file(file_path)

    loaded_sample_path: str = ""
    def load_sample_file(self, file:str):
        '''파일 설정'''
        self.loaded_sample_path = file
        try:
            with open(file, "r", encoding='utf8') as f:
                self.text_source.setPlainText(f.read())
        except :
            try:
                with open(file, "r") as f:
                    self.text_source.setPlainText(f.read())
            except :
                self.output_log(LOG_TYPE.LOG, f"{file} 파일을 읽을 수 없습니다.")

    def save_sample_file(self, file:str):
        '''파일 저장'''
        if file == self.loaded_sample_path:
            try:
                with open(file, "w", encoding='utf8') as f:
                    f.write(self.text_source.toPlainText())
                self.output_log(LOG_TYPE.LOG, f"{file} 저장완료")
            except :
                self.output_log(LOG_TYPE.LOG, f"{file} 저장실패")

    async def set_code(self, ident:str):
        tr_prop = self.map_trprops.get(ident)
        if tr_prop is None:
            self.doc_desc.setText(f"{ident}: not founded")
            self.text_source.setPlainText(f"# {ident}: not founded")
            return
        self.cur_tr_prop = tr_prop
        tr_cd = tr_prop['trCode']
        tr_name = tr_prop['trName']
        tr_path = tr_prop['.parent']['accessUrl']
        isWebsocket = tr_path.startswith("/websocket")
        if isWebsocket:
            self.doc_desc.setText(f"{tr_cd}: {tr_name}, URL: /websocket")
        else:
            self.doc_desc.setText(f"{tr_cd}: {tr_name}, 초당: {tr_prop['transactionPerSec']}, path: {tr_path}")
        res_text = tr_prop.get('res_text')
        if res_text is None:
            fieldProps = await LSSiteHelper.GetFieldProps(tr_prop['id'])
            tr_prop['fieldProps'] = fieldProps
            inblocks = list[BlockRecord]()
            outblocks = list[BlockRecord]()
            InblockRecord = None
            OutblockRecord = None
            if isWebsocket:
                InblockRecord = BlockRecord(f"{tr_cd}InBlock", "object", [])
                OutblockRecord = BlockRecord(f"{tr_cd}OutBlock", "object", [])
            for field in fieldProps:
                propertyLength = field.get('propertyLength')
                if field['bodyType'] == 'req_b':
                    if propertyLength is None:
                        if InblockRecord is not None:
                            inblocks.append(InblockRecord)
                        InblockRecord = BlockRecord(field['propertyCd'].strip(), LSSiteHelper.GetDataType(field['propertyType']), [])
                    else:
                        size = propertyLength.strip()
                        code = field['propertyCd'].replace('&nbsp;', '').replace('-', '')
                        name = field['propertyNm']
                        desc = field.get('description')
                        if desc is not None:
                            desc = desc.replace('<br/>', '\n')
                        else:
                            desc = ''
                        filedInfo = BlockFieldInfo(code, name, desc, LSSiteHelper.GetDataType(field['propertyType']), size)
                        if InblockRecord:
                            InblockRecord.fields.append(filedInfo)
                elif field['bodyType'] == 'res_b':
                    if propertyLength is None:
                        if OutblockRecord is not None:
                            outblocks.append(OutblockRecord)
                        OutblockRecord = BlockRecord(field['propertyCd'].strip(), LSSiteHelper.GetDataType(field['propertyType']), [])
                    else:
                        size = propertyLength.strip()
                        code = field['propertyCd'].replace('&nbsp;', '').replace('-', '')
                        name = field['propertyNm']
                        desc = field.get('description')
                        if desc is not None:
                            desc = desc.replace('<br/>', '\n')
                        else:
                            desc = ''
                        filedInfo = BlockFieldInfo(code, name, desc, LSSiteHelper.GetDataType(field['propertyType']), size)
                        if OutblockRecord:
                            OutblockRecord.fields.append(filedInfo)

            if InblockRecord is not None:
                inblocks.append(InblockRecord)
            if OutblockRecord is not None:
                outblocks.append(OutblockRecord)

            res_text = str()
            blocks = inblocks + outblocks
            for block in blocks:
                res_text += f"{block.name}: {block.obj_type}\n"
                table = PrettyTable(hrules=1)
                table.field_names = ['element', 'name', 'type', 'size', 'desc']
                table.add_rows([[x.code, x.name, x.var_type, x.size, x.desc ]for x in block.fields])
                res_text += table.get_string()
                res_text += '\n\n'

            tr_prop['inblocks'] = inblocks
            tr_prop['outblocks'] = outblocks
            tr_prop['res_text'] = res_text

        if self.check_show_res_flag.isChecked():
            self.text_result.setPlainText(res_text)

        src_text = str()
        if isWebsocket:
            char_sum = 0
            for c in tr_cd:
                char_sum += ord(c)
            back_filepath = self.backup_folder + f"\\{tr_cd}{char_sum}.txt"
            if os.path.exists(back_filepath):
                try:
                    with open(back_filepath, "r", encoding='utf8') as f:
                        src_text = f.read()
                except :
                    pass
                self.text_source.setPlainText(src_text)
            if len(src_text) < 10:
                src_text += f"""async def sample(api):
    # 실시간 등록
    key = '' # 단축코드 6자리 또는 8자리 (단건, 연속), (계좌등록/해제 일 경우 필수값 아님)
    ok = await api.add_realtime('{tr_cd}', key) 
    if not ok:
        return print(f'실시간 등록 실패: {{api.last_message}}')
    print('실시간 등록 성공, 10초간 실시간 수신')

    # 10초간 실시간 수신
    await asyncio.sleep(10)

    # 실시간 해제
    await api.remove_realtime('{tr_cd}', key)
    print('실시간 해제')
"""
        else:
            back_filepath = self.backup_folder + f"\\{tr_cd}.txt"
            if os.path.exists(back_filepath):
                try:
                    with open(back_filepath, "r", encoding='utf8') as f:
                        src_text = f.read()
                except :
                    pass
                self.text_source.setPlainText(src_text)
            if len(src_text) < 10:
                src_text = ""
                src_text += "async def sample(api):\n"
                src_text += "    inputs = {\n"
                inblocks: list[BlockRecord] = tr_prop['inblocks']
                for block in inblocks:
                    is_occurs = block.obj_type == 'object_array'
                    if is_occurs:
                        src_text += f"        '{block.name}': [\n"
                        src_text += "            {\n"
                        for field in block.fields:
                            if field.var_type == 'number':
                                src_text += f"                '{field.code}': 0, # {field.name}\n"
                            else:
                                src_text += f"                '{field.code}': '', # {field.name}\n"
                        src_text += "            },\n"
                        src_text += "        ],\n"
                    else:
                        src_text += f"        '{block.name}': {{\n"
                        for field in block.fields:
                            if field.var_type == 'number':
                                src_text += f"            '{field.code}': 0, # {field.name}\n"
                            else:
                                src_text += f"            '{field.code}': '', # {field.name}\n"
                        src_text += '        },\n'
                src_text += "    }\n"
                src_text += f"    response = await api.request('{tr_cd}', inputs)\n"
                src_text += "    if not response: return print(f'요청 실패: {api.last_message}')\n"
                src_text += "    \n"
                src_text += "    print(response)\n"
        self.text_source.setPlainText(src_text)

    @asyncSlot()
    async def func_remove_realtime(self):
        '''실시간 중지'''
        list_widget = self.list_event_realtime
        selected = list_widget.selectedItems()
        if len(selected) < 1:
            return
        first_text = selected[0].text()
        words = first_text.split(": ")
        if len(words) > 1:
            real_msg = words[1]
            real_msg = real_msg.split(", ")
            if len(real_msg) > 1:
                code = real_msg[0]
                key = real_msg[1]
                await self.api.remove_realtime(code, key)

    @asyncSlot(QListWidgetItem)
    async def on_log_double_click(self, item:QListWidgetItem):
        '''로그 더블클릭'''
        words = item.text().split(": ")
        if len(words) > 2:
            action = words[1]
            if action == "코드실행":
                code = words[2]
                await self.set_code(code)

    @asyncSlot()
    async def set_macaddress(self) -> str:
        '''MacAddress 설정'''
        text, ok = await QAsyncDialog.getText(self, 'MacAddress설정', "법인경우 필수 세팅 (12자리)", self.mac_address)
        if ok:
            self.api.mac_address = text

    @asyncSlot()
    async def tool_action(self, action_name:str):
        self.output_log(LOG_TYPE.LOG, f"Tool: {action_name}")
        if action_name == "전체 URL":
            lines = list[str]()
            lines.append("tr_code_to_path:dict = {")
            lines.append("")
            for root_group in self.root_groups:
                for subgroup in root_group.sub_groupList:
                    subgroup_name = subgroup['name']
                    subgroup_url = subgroup['accessUrl']
                    subgroup_protocolType = subgroup['protocolType']
                    is_websockt = subgroup_protocolType == "WEBSOCKET"
                    lines.append(f"    # {subgroup_name}")
                    for tr_prop in subgroup['tr_props']:
                        if is_websockt:
                            lines.append(f'    "{tr_prop['trCode']}" : "/websocket",')
                        else:
                            lines.append(f'    "{tr_prop['trCode']}" : "{subgroup_url}",')
                    lines.append("")
            lines.append("}")
            lines.append("")
            self.text_result.setPlainText("\n".join(lines))
        elif action_name == "TR필드":
            if self.cur_tr_prop is not None:
                blocks = self.cur_tr_prop['inblocks'] + self.cur_tr_prop['outblocks']
                lines = list[str]()
                for block in blocks:
                    lines.append(f"# {block.name}: {block.obj_type}")
                    lines.append(f"{block.name}_field_count = {len(block.fields)}")
                    lines.append(f"{block.name}_elements = [{', '.join([f'"{x.code}"' for x in block.fields])}]")
                    lines.append(f"{block.name}_names = [{', '.join([f'"{x.name}"' for x in block.fields])}]")
                    lines.append("")
                self.text_result.setPlainText("\n".join(lines))
            else:
                self.text_result.setPlainText("# TR 선택 필수")
        elif action_name == "TEST":
            pass
        pass

    @asyncSlot()
    async def func_profile_login(self, profile_index:int):
        '''프로필 로그인'''
        profile_obj = self.settings.get(f"Profile {profile_index+1}")

        if profile_obj is None:
            return

        # show ProfileWindow
        name = profile_obj["name"]
        try:
            appkey = self.cipher_suite.decrypt(profile_obj["appkey"].encode()).decode()
            appsecretkey = self.cipher_suite.decrypt(profile_obj["appsecretkey"].encode()).decode()
        except :
            appkey = ""
            appsecretkey = ""
        remember = profile_obj["remember"]

        dialog = ProfileDialog(self)
        dialog.text_name.setText(name)
        dialog.text_appkey.setText(appkey)
        dialog.text_appsecretkey.setText(appsecretkey)
        dialog.check_remember.setChecked(remember)

        result = await QAsyncDialog.dialog_async_exec(dialog)

        name = dialog.text_name.text()
        appkey = dialog.text_appkey.text()
        appsecretkey = dialog.text_appsecretkey.text()
        remember = dialog.check_remember.isChecked()

        if not remember:
            profile_obj["appkey"] = ""
            profile_obj["appsecretkey"] = ""
        profile_obj["remember"] = remember

        if result == QDialog.DialogCode.Accepted:
            for i in range(self.profile_count):
                if i == profile_index:
                    continue
                if self.menu_profiles[i].text() == name:
                    self.output_log(LOG_TYPE.LOG, f"프로필네임 {name} 중복")
                    return

            self.menu_profiles[profile_index].setText(name)
            profile_obj["name"] = name
            if remember:
                profile_obj["appkey"] = self.cipher_suite.encrypt(appkey.encode()).decode()
                profile_obj["appsecretkey"] = self.cipher_suite.encrypt(appsecretkey.encode()).decode()

            self.output_log(LOG_TYPE.LOG, f"{name} 로그인중...")
            ok = await self.api.login(appkey, appsecretkey)
            if ok:
                self.output_log(LOG_TYPE.LOG, f"{name} 로그인성공: {"모의투자" if self.api.is_simulation else "실투자"}")
            else:
                self.output_log(LOG_TYPE.LOG, f"{name} 로그인실패: {self.api.last_message}")

            self.login_menu.setEnabled(not ok)

    @asyncSlot()
    async def func_logout(self):
        '''로그아웃'''
        if not self.api.connected:
            return
        await self.api.close()
        self.output_log(LOG_TYPE.LOG, "로그아웃")
        self.login_menu.setEnabled(True)

    @asyncSlot()
    async def func_run(self):
        ''' 코드실행 '''
        self.btn_run.setEnabled(False)
        if self.check_clear_flag.isChecked():
            self.text_result.clear()

        src_code = self.text_source.toPlainText()
        is_tr_request = False
        tr_prop = self.cur_tr_prop
        if tr_prop is not None:
            tr_cd = tr_prop['trCode']
            tr_name = tr_prop['trName']
            tr_path = tr_prop['.parent']['accessUrl']
            isWebsocket = tr_path.startswith("/websocket")
            is_tr_request = not isWebsocket
            self.output_log(LOG_TYPE.LOG, f"코드실행: {tr_cd}: {tr_name}")
            # 백업
            filename = tr_cd
            if isWebsocket:
                char_sum = 0
                for c in tr_cd:
                    char_sum += ord(c)
                filename = f"{tr_cd}{char_sum}"

            back_filepath = self.backup_folder + f"\\{filename}.txt"
            try:
                if len(src_code) > 100:
                    with open(back_filepath, "w", encoding='utf8') as f:
                        f.write(src_code)
                else:
                    if os.path.exists(back_filepath):
                        # delete backup file
                        os.remove(back_filepath)
            except:
                self.output_log(LOG_TYPE.LOG, f"백업실패: {back_filepath}")
        else:
            if self.cur_sample:
                self.output_log(LOG_TYPE.LOG, f"코드실행: 샘플코드: {self.cur_sample}")
            else:
                self.output_log(LOG_TYPE.LOG, "코드실행: 사용자 코드")
        # 소스 텍스트를 실행
        try:
            module = types.ModuleType('test')
            exec(src_code, module.__dict__)
            # check loaded asyncio module
            if not hasattr(module, "asyncio"):
                setattr(module, "asyncio", asyncio)
            if "sample" not in dir(module):
                self.appent_result_line("# 실행 오류: sample 함수가 없습니다.")
                self.btn_run.setEnabled(True)
                return
            module.__dict__['print'] = custom_print
            if asyncio.iscoroutinefunction(module.sample):
                await module.sample(self.api)
            else:
                module.sample(self.api)
        except Exception as e:
            err_msg = e.message if hasattr(e, 'message') else str(e)
            self.appent_result_line(f"# 실행 오류: {err_msg}")

        if is_tr_request:
            last_response = self.api._last_respose_value
            if last_response is not None and last_response.tr_cd == tr_cd:
                # 테스트베드에 응답출력
                self.text_test_in_tr_cd.setText(tr_cd)
                self.text_test_path.setText(last_response.path)
                self.text_test_in_tr_cont_yn.setText(last_response.in_tr_cont)
                self.text_test_in_tr_cont_key.setText(last_response.in_tr_cont_key)
                self.text_test_request.setPlainText(last_response.request_text)
                self.text_test_out_tr_cont_yn.setText(last_response.tr_cont)
                self.text_test_out_tr_cont_key.setText(last_response.tr_cont_key)
                self.text_test_response.setPlainText(last_response.response_text)
                self.text_test_request_time.setText(f"요청시간: {datetime.fromtimestamp(last_response.request_time).strftime("%H:%M:%S.%f")[:-3]}")
                self.text_test_response_time.setText(f"응답시간(ms): {last_response.elapsed_ms}")
        self.btn_run.setEnabled(True)

    @asyncSlot()
    async def func_test_request(self):
        '''테스트베드 요청'''
        path = self.text_test_path.text()
        tr_cd = self.text_test_in_tr_cd.text()
        tr_cont_yn = self.text_test_in_tr_cont_yn.text()
        tr_cont_key = self.text_test_in_tr_cont_key.text()
        request_text = self.text_test_request.toPlainText()

        response = await self.api.request(tr_cd, request_text, path=path, tr_cont=tr_cont_yn, tr_cont_key=tr_cont_key)
        if response is None:
            self.text_test_response.setPlainText(f"요청실패: {self.api.last_message}")
            return

        self.text_test_out_tr_cont_yn.setText(response.tr_cont)
        self.text_test_out_tr_cont_key.setText(response.tr_cont_key)
        self.text_test_response.setPlainText(response.response_text)
        self.text_test_request_time.setText(f"요청시간: {datetime.fromtimestamp(response.request_time).strftime('%H:%M:%S.%f')[:-3]}")
        self.text_test_response_time.setText(f"응답시간(ms): {response.elapsed_ms}")

class QAsyncDialog:
    @staticmethod
    def dialog_async_exec(dialog):
        future = asyncio.Future()
        dialog.finished.connect(lambda r: future.set_result(r))
        dialog.open()
        return future

    @staticmethod
    async def getText(parent, title, label, text=''):
        """ 비동기 방식으로 메시지 박스를 띄운다. """
        dialog = QInputDialog(parent)
        dialog.setWindowTitle(title)
        dialog.setLabelText(label)
        dialog.setTextValue(text)
        result = await QAsyncDialog.dialog_async_exec(dialog)
        return dialog.textValue(), result

class ProfileDialog(QDialog):
    def __init__(self, parent:QWidget):
        super().__init__(parent)
        self.setWindowTitle("프로필 설정")
        self.resize(400, 180)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        layout = QFormLayout()
        self.text_name = QLineEdit()
        self.text_appkey = QLineEdit()
        self.text_appsecretkey = QLineEdit()
        self.check_remember = QCheckBox("remember keys")

        layout.addRow("Profile name", self.text_name)
        layout.addRow("AppKey", self.text_appkey)
        layout.addRow("AppSecretKey", self.text_appsecretkey)
        layout.addItem(QSpacerItem(0, 10))
        layout.addRow("Remember", self.check_remember)
        self.setLayout(layout)
        self.btn_ok = QPushButton("확인")
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel = QPushButton("취소")
        self.btn_cancel.clicked.connect(self.close)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.btn_ok)
        layout2.addWidget(self.btn_cancel)
        layout.addRow(layout2)

class BlockFieldInfo:
    def __init__(self, code:str, name:str, desc:str, var_type:str, size:str):
        self.code = code
        self.name = name
        self.desc = desc
        self.var_type = var_type
        self.size = size

class BlockRecord:
    def __init__(self, name:str, obj_type:str, fields:list[BlockFieldInfo]):
        self.name = name
        self.obj_type = obj_type
        self.fields = fields

class RootGroup:
    def __init__(self, group_id:str, desc_name:str):
        self.id = group_id
        self.desc_name = desc_name
        self.sub_groupList = list()
    def __str__(self):
        return f"{self.group_id}: {self.desc_name}"
    def __repr__(self):
        return self.__str__()
    def add_sub_group(self, sub_group):
        self.sub_groupList.append(sub_group)

class LSSiteHelper:
    URL_BASE = "https://openapi.ls-sec.co.kr"
    httpclient:aiohttp.ClientSession = None

    @staticmethod
    def initialize():
        LSSiteHelper.httpclient = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10))

    @staticmethod
    async def GetApiGuide():
        response = await LSSiteHelper.httpclient.get(LSSiteHelper.URL_BASE + "/apiservice")
        if response.status != 200:
            return None
        return await response.text()

    @staticmethod
    async def GetRootGroups():
        api_guide = await LSSiteHelper.GetApiGuide()
        root_groupList = list[RootGroup]()
        if api_guide is None:
            return root_groupList
        loadApiList_pos = api_guide.find("loadApiList(")
        while loadApiList_pos > 0:
            first_param_pos = api_guide.find(",", loadApiList_pos)
            if first_param_pos < 0:
                break

            first_param = api_guide[loadApiList_pos + 12:first_param_pos]
            group_id = first_param.replace("&quot;", "")

            desc_name_pos = api_guide.find(">", first_param_pos)
            if desc_name_pos < 0:
                break

            desc_name_end = api_guide.find("</a>", desc_name_pos)
            if desc_name_end < 0:
                break

            desc_name = api_guide[desc_name_pos + 1:desc_name_end]

            if len(group_id) == 36:
                root_groupList.append(RootGroup(group_id, desc_name))

            loadApiList_pos = api_guide.find("loadApiList(", desc_name_end)

        return root_groupList

    @staticmethod
    async def GetApiInfo(url) -> list | dict:
        response = await LSSiteHelper.httpclient.get(LSSiteHelper.URL_BASE + url)
        if response.status != 200:
            return None
        return await response.json()

    @staticmethod
    def GetSubGroups(group_id: str):
        return LSSiteHelper.GetApiInfo(f"/api/apis/public/api-list/{group_id}")

    @staticmethod
    def GetTrProps(group_id: str):
        return LSSiteHelper.GetApiInfo(f"/api/apis/guide/tr/{group_id}")

    @staticmethod
    def GetFieldProps(tr_id: str):
        return LSSiteHelper.GetApiInfo(f"/api/apis/guide/tr/property/{tr_id}")

    @staticmethod
    def GetDataType(orgName:str):
        match orgName:
            case "A0001":
                return "str"
            case "A0002":
                return "array"
            case "A0003":
                return "object"
            case "A0004":
                return "number"
            case "A0005":
                return "object_array"
            case _:
                return "unknown"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    window = MainWindow()
    window.show()

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(window.initalize_async())
        loop.run_forever()
