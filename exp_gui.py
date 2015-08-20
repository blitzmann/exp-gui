import os
import wx
import json

json_path = r"."

with open(os.path.join(json_path, "dgmexpressions.json"), mode='r', encoding="utf8") as file:
    dgmexpressions = {}
    for row in json.load(file):
        dgmexpressions[row['expressionID']] = row

with open(os.path.join(json_path, 'dgmeffects.json'), mode='r', encoding="utf8") as file:
    dgmeffects = {}
    for row in json.load(file):
        dgmeffects[row['effectID']] = row

effect_id_name = {}
for id, row in dgmeffects.items():
    effect_id_name[row['effectName']] = row['effectID']

'''
operand_search = 41

# Search for effects using the defined operand. Only works if the operand is at root of expression
for _, expression in dgmexpressions.items():
    if expression['operandID'] == operand_search:
        for _, effect in dgmeffects.items():
            if expression['expressionID'] == effect['preExpression'] or expression['expressionID'] == effect['postExpression']:
                print(effect['effectName'])
'''

class TreePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)
        self.expressionTree = ExpressionTree(self, self)
        vbox.Add(self.expressionTree, 1, wx.EXPAND)

class ExpressionTree(wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        self.root = self.AddRoot("root")

        # self.loadEffect('eliteBonusGunshipLaserDamage2')
        # Bind our lookup method to when the tree gets expanded
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.expandLookup)

    def loadEffect(self, info, effectID=False):
        self.DeleteChildren(self.root)
        if info not in effect_id_name and not effectID:
            return

        if effectID:
            childId = self.AppendItem(self.root, "expressionID: {}".format(info), data=int(info))
            self.AppendItem(childId, "dummy")
        else:
            effect_id = effect_id_name[info]

            for k, v in dgmeffects[effect_id].items():
                if k not in ('preExpression', 'postExpression'):
                    continue
                childId = self.AppendItem(self.root, "{}: {}".format(k, v), data=v)
                self.AppendItem(childId, "dummy")

    def expandLookup(self, event):
        """Process expression tree expansions"""
        root = event.Item
        child = self.GetFirstChild(root)[0]
        # If child of given group is a dummy
        if self.GetItemText(child) == "dummy":
            # Delete it
            self.Delete(child)
            # And add real contents
            children = dgmexpressions[self.GetItemData(root)]

            for k,v in children.items():
                if v is not None and v != '':
                    childId = self.AppendItem(root, "{}: {}".format(k, v), data=v)
                    if k in ("arg1", "arg2") and v is not None:
                        self.AppendItem(childId, "dummy")

            self.SortChildren(root)

class MainFrame(wx.Frame):
    __instance = None

    @classmethod
    def getInstance(cls):
        return cls.__instance if cls.__instance is not None else MainFrame()

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Expression Tree GUI", size=wx.Size(1000, 500))

        MainFrame.__instance = self

        #Fix for msw (have the frame background color match panel color
        if 'wxMSW' in wx.PlatformInfo:
            self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.txt_filter = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, style=wx.TE_PROCESS_ENTER)
        self.txt_filter.AutoComplete(list(effect_id_name.keys()))
        sizer.Add(self.txt_filter, 1, wx.ALL | wx.EXPAND, 5)

        self.btn = wx.Button(self, wx.ID_ANY, "effectName", wx.DefaultPosition)
        sizer.Add(self.btn, 0, wx.ALL | wx.EXPAND, 5)

        self.btn2 = wx.Button(self, wx.ID_ANY, "expressionID", wx.DefaultPosition)
        sizer.Add(self.btn2, 0, wx.ALL | wx.EXPAND, 5)

        main_sizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 5)

        self.tree = ExpressionTree(self,)
        main_sizer.Add(self.tree, 1, wx.ALL | wx.EXPAND, 5)

        self.txt_filter.Bind(wx.EVT_TEXT_ENTER, self.textbox)
        self.btn.Bind(wx.EVT_BUTTON, self.textbox)
        self.btn2.Bind(wx.EVT_BUTTON, self.textbox2)

        self.SetSizer(main_sizer)
        self.Layout()

        self.Centre(wx.BOTH)
        self.Show()


    def textbox(self, event):
        text = self.txt_filter.GetValue()
        self.tree.loadEffect(text, False)

    def textbox2(self, event):
        text = self.txt_filter.GetValue()
        self.tree.loadEffect(text, True)

    def OnClose(self, event):
        event.Skip()

gui = wx.App(False)
MainFrame()
gui.MainLoop()
