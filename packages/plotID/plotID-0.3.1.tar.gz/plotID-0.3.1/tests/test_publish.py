# -*- coding: utf-8 -*-

"""
Unittests for publish
"""

import unittest
import os
import sys
import platform
import shutil
from collections import Counter
from importlib.metadata import version
from subprocess import run, CalledProcessError
from unittest.mock import patch
import re
import matplotlib.pyplot as plt
from plotid.publish import (
    publish,
    PublishOptions,
    find_plotid_calls,
    find_pattern,
    comment_lines,
)
from plotid.plotoptions import PlotIDTransfer


SRC_DIR = "test_src_folder"
SRC_FILES = ["test_file1.txt", "test_file2.jpg", "test_file3.exe"]
PIC_NAME = "test_picture"
DST_DIR = "test_dst_folder"
DST_PARENT_DIR = "test_parent"
DST_PATH = os.path.join(DST_PARENT_DIR, DST_DIR)
FIG = plt.figure(figsize=[6.4, 4.8], dpi=100)
FIG2 = plt.figure(figsize=[6.4, 4.8], dpi=100)
FIGS_AS_LIST = [FIG, FIG2]
IDS_AS_LIST = ["MR05_0x63203c6f", "MR05_0x63203c70"]
FIGS_AND_IDS = PlotIDTransfer(FIGS_AS_LIST, IDS_AS_LIST)
PIC_NAME_LIST = [PIC_NAME, "second_picture"]
DST_DIR = os.path.abspath(os.path.join("tests", "test_comment"))
TEXT_FILE = "tmp_test_find_lines.txt"
PYTHON_FILE = "tmp_test_find_calls.py"


class TestPublish(unittest.TestCase):
    """
    Class for all unittests of the publish module.
    """

    def setUp(self) -> None:
        """Generate source and destination directory and source files."""
        os.makedirs(SRC_DIR, exist_ok=True)
        os.makedirs(DST_PARENT_DIR, exist_ok=True)
        for file in SRC_FILES:
            with open(file, "w", encoding="utf-8"):
                pass

        os.mkdir(DST_DIR)
        with open(TEXT_FILE, "x", encoding="utf-8") as file:
            content = (
                "Lorem ipsum(\ndolor\nsit() amet(,\nconsectetur) adipisici )elit, sed "
                "eiusmod tempor\nincidunt ut\nlab\nore et dolore\nmagna aliqua."
            )
            file.write(content)
        with open(PYTHON_FILE, "x", encoding="utf-8") as file:
            content = (
                "import sys\nfrom plotid.tagplot import tagplot\nimport plotid\n"
                "x=123\ns='abc'\npublish(\n'Lorem ipsum',\nx+1 (\n)  )"
                "  \ntagplot()\n \n\n\ntagplot(()) \nsys.exit()"
            )
            file.write(content)

    # Skip test if tests are run from command line.
    @unittest.skipIf(
        not os.path.isfile(sys.argv[0]),
        "Publish is not called from a Python script. Therefore, the script cannot be "
        "copied.",
    )
    def test_publish(self) -> None:
        """
        Test publish and check if an exported picture file exists.
        The destination path is given with trailing slash.
        """
        publish(
            PlotIDTransfer(FIG, "testID"),
            SRC_DIR,
            DST_PATH + "/",
            plot_names=PIC_NAME,
            data_storage="individual",
        )
        assert os.path.isfile(os.path.join(DST_PATH, "testID", PIC_NAME + ".png"))

    # Skip test if tests are run from command line.
    @unittest.skipIf(
        not os.path.isfile(sys.argv[0]),
        "Publish is not called "
        "from a Python script. Therefore, the script cannot be "
        "copied.",
    )
    def test_publish_multiple_figs_custom_name(self) -> None:
        """
        Test publish with multiple figures and check if all exported picture
        files exist with the provided strings as their names.
        """
        publish(FIGS_AND_IDS, SRC_DIR, DST_PATH, plot_names=PIC_NAME_LIST)
        for i, name in enumerate(PIC_NAME_LIST):
            assert os.path.isfile(os.path.join(DST_PATH, IDS_AS_LIST[i], name + ".png"))

    # Skip test if tests are run from command line.
    @unittest.skipIf(
        not os.path.isfile(sys.argv[0]),
        "Publish is not called "
        "from a Python script. Therefore, the script cannot be "
        "copied.",
    )
    def test_publish_multiple_figs_standard_name(self) -> None:
        """
        Test publish with multiple figures and check if all exported picture
        files exist with the IDs as their names.
        """
        publish(FIGS_AND_IDS, SRC_DIR, DST_PATH)
        for identifier in IDS_AS_LIST:
            assert os.path.isfile(
                os.path.join(DST_PATH, identifier, identifier + ".png")
            )

    def test_figs_and_ids(self) -> None:
        """
        Test if RuntimeError is raised when figs_and_ids is not an
        PlotIDTransfer object.
        """
        with self.assertRaises(RuntimeError):
            publish("FIGS_AND_IDS", SRC_DIR, DST_PATH)

    def test_wrong_ids(self) -> None:
        """Test if Error is raised if IDs are of wrong type."""
        with self.assertRaises(TypeError):
            publish(PlotIDTransfer(FIG, 3), SRC_DIR, DST_PATH)
        with self.assertRaises(TypeError):
            publish(PlotIDTransfer(FIG, ["i", 4]), SRC_DIR, DST_PATH)

    # Skip test if tests are run from command line.
    @unittest.skipIf(
        not os.path.isfile(sys.argv[0]),
        "Publish is not called from a Python script. Therefore, the script cannot be "
        "copied.",
    )
    def test_publish_multiple_src_files(self) -> None:
        """
        Test publish with multiple source files and check
        if the exported data files exist.
        """
        files_and_dir = list(SRC_FILES)
        files_and_dir.append(SRC_DIR)
        publish(
            FIGS_AND_IDS,
            files_and_dir,
            DST_PATH,
            plot_names=PIC_NAME_LIST,
            data_storage="individual",
        )
        for identifier in IDS_AS_LIST:
            for file in SRC_FILES:
                path = os.path.join(DST_PATH, identifier)
                assert os.path.isdir(path)
                assert os.path.isfile(os.path.join(path, file))

    def test_src_directory(self) -> None:
        """Test if Error is raised when source directory does not exist."""
        with self.assertRaises(FileNotFoundError):
            publish(FIGS_AND_IDS, "not_existing_folder", DST_PATH)

    # Skip test if tests are run from command line.
    @unittest.skipIf(
        not os.path.isfile(sys.argv[0]),
        "Publish is not called from a Python script. Therefore, the script cannot be "
        "copied.",
    )
    def test_src_directory_type(self) -> None:
        """Test if Error is raised when source directory is not a string."""
        with self.assertRaises(TypeError):
            publish(FIGS_AND_IDS, [SRC_DIR, 4], DST_PATH)
        with self.assertRaises(TypeError):
            publish(FIGS_AND_IDS, 4, DST_PATH)

    def test_dst_directory(self) -> None:
        """
        Test if Error is raised when the directory above the
        destination dir does not exist.
        """
        with self.assertRaises(FileNotFoundError):
            publish(FIGS_AND_IDS, SRC_DIR, "not_existing_folder/data")

    def test_script_exists(self) -> None:
        """
        Test if Error is raised when publish is called from a shell.

        First publish is called from a python shell with correct parameters.
        It is checked if the subprocess returns an Error. Since the type of
        exception is not passed but a CalledProcessError is raised, publish
        is called again and it is checked if the output contains the correct
        exception type.
        """
        if platform.system() == "Linux":
            python = "python3"
        else:
            python = "python"

        with self.assertRaises(CalledProcessError):
            run(
                [
                    python,
                    "-c",
                    "import matplotlib.pyplot as plt\n"
                    "from plotid.publish import publish\n"
                    "from plotid.plotoptions import PlotIDTransfer\n"
                    "publish(PlotIDTransfer(plt.figure(), 'testID2'),"
                    " 'test_src_folder', 'test_parent/test_dst_folder')",
                ],
                capture_output=True,
                check=True,
            )
        process = run(
            [
                python,
                "-c",
                "import matplotlib.pyplot as plt\n"
                "from plotid.publish import publish\n"
                "from plotid.plotoptions import PlotIDTransfer\n"
                "publish(PlotIDTransfer(plt.figure(), 'testID2'), "
                "'test_src_folder', 'test_parent/test_dst_folder')",
            ],
            capture_output=True,
        )
        assert (
            "FileNotFoundError: Cannot copy original python script. "
            "Running publish from a shell"
            " is not possible."
        ) in process.stderr.decode()

    # Skip test if tests are run from command line.
    @unittest.skipIf(
        not os.path.isfile(sys.argv[0]),
        "Publish is not called "
        "from a Python script. Therefore, the script cannot be "
        "copied.",
    )
    def test_dst_already_exists_yes(self) -> None:
        """
        Test if publish succeeds if the user wants to overwrite an existing
        destination directory.
        """
        os.mkdir(DST_PATH)
        os.mkdir(os.path.join(DST_PATH, IDS_AS_LIST[0]))
        # Mock user input as 'yes'
        with patch("builtins.input", return_value="yes"):
            publish(FIGS_AND_IDS, SRC_DIR, DST_PATH, data_storage="individual")

    # Skip test if tests are run from command line.
    @unittest.skipIf(
        not os.path.isfile(sys.argv[0]),
        "Publish is not called "
        "from a Python script. Therefore, the script cannot be "
        "copied.",
    )
    def test_dst_already_exists_no(self) -> None:
        """
        Test if publish exits with error if the user does not want to overwrite
        an existing destination directory by user input 'no'.
        """
        os.mkdir(DST_PATH)
        os.mkdir(os.path.join(DST_PATH, IDS_AS_LIST[0]))
        os.mkdir(os.path.join(DST_PATH, IDS_AS_LIST[1]))
        # Mock user input as 'no'
        with patch("builtins.input", return_value="no"):
            with self.assertRaises(RuntimeError):
                publish(FIGS_AND_IDS, SRC_DIR, DST_PATH)

    # Skip test if tests are run from command line.
    @unittest.skipIf(
        not os.path.isfile(sys.argv[0]),
        "Publish is not called "
        "from a Python script. Therefore, the script cannot be "
        "copied.",
    )
    def test_dst_already_exists_empty(self) -> None:
        """
        Test if publish exits with error if the user does not want to overwrite
        an existing destination directory by missing user input.
        """
        os.mkdir(DST_PATH)
        os.mkdir(os.path.join(DST_PATH, IDS_AS_LIST[0]))
        os.mkdir(os.path.join(DST_PATH, IDS_AS_LIST[1]))
        # Mock user input as empty (no should be default).
        with patch("builtins.input", return_value=""):
            with self.assertRaises(RuntimeError):
                publish(FIGS_AND_IDS, SRC_DIR, DST_PATH, data_storage="individual")

    # Skip test if tests are run from command line.
    @unittest.skipIf(
        not os.path.isfile(sys.argv[0]),
        "Publish is not called from a Python script. Therefore, the script cannot be "
        "copied.",
    )
    def test_dst_invisible_already_exists(self) -> None:
        """
        Test if after a crash of publish the partially copied data is
        removed.
        To mock this, the invisible directory already exists.
        """
        os.mkdir(DST_PATH)
        invisible_path1 = os.path.join(DST_PATH, "." + IDS_AS_LIST[0])
        os.mkdir(invisible_path1)
        # Mock user input as 'yes' for deleting the partial copied data
        with patch("builtins.input", side_effect=["yes", "yes"]):
            with self.assertRaises(RuntimeError):
                publish(FIGS_AND_IDS, SRC_DIR, DST_PATH, plot_names=PIC_NAME)
        assert not os.path.isdir(invisible_path1)
        os.remove("test_picture1.tmp.png")
        os.remove("test_picture2.tmp.png")

    def test_plot_names(self) -> None:
        """Test if Error is raised if plot_name is not a string."""
        with self.assertRaises(TypeError):
            publish(
                FIGS_AND_IDS,
                SRC_DIR,
                DST_PATH,
                plot_names=7.6,
                data_storage="individual",
            )
        with self.assertRaises(TypeError):
            publish(FIGS_AND_IDS, SRC_DIR, DST_PATH, plot_names=())
        with self.assertRaises(TypeError):
            publish(FIGS_AND_IDS, SRC_DIR, DST_PATH, plot_names=["test", 3])

    # Skip test if tests are run from command line.
    @unittest.skipIf(
        not os.path.isfile(sys.argv[0]),
        "Publish is not called from a Python script. Therefore, the script cannot be "
        "copied.",
    )
    def test_data_storage(self) -> None:
        """
        Test if Error is raised when unsupported storage method was chosen.
        """
        with self.assertRaises(ValueError):
            publish(
                FIGS_AND_IDS, SRC_DIR, DST_PATH, data_storage="none_existing_method"
            )
        with self.assertRaises(TypeError):
            publish(FIGS_AND_IDS, SRC_DIR, DST_PATH, data_storage=3)
        with self.assertRaises(TypeError):
            publish(FIGS_AND_IDS, SRC_DIR, DST_PATH, data_storage=[])

    def test_str(self) -> None:
        """
        Test if the string representation of a PublishOptions object is
        correct.
        """
        self.maxDiff = None
        publish_obj = PublishOptions(FIGS_AND_IDS, SRC_DIR, DST_PATH)
        self.assertIn(
            "<class 'plotid.publish.PublishOptions'>: {'figure': "
            "[<Figure size 640x480 with 0 Axes>, <Figure size"
            " 640x480 with 0 Axes>], 'figure_ids': "
            "['MR05_0x63203c6f', 'MR05_0x63203c70'], "
            "'src_datapaths': 'test_src_folder'",
            str(publish_obj),
        )

    def test_export_imports(self) -> None:
        """
        Test if imports of the calling script are correctly written to file.
        This test only works if called from the parent directory, since the path to the
        file to test the behaviour has to be specified correctly.
        """
        mpl_version = version("matplotlib")
        expected_modules = [
            "shutil\n",
            "unittest\n",
            "subprocess\n",
            "platform\n",
            f"matplotlib=={mpl_version}\n",
            "os\n",
            "re\n",
            "sys\n",
            "collections\n",
            "importlib\n",
        ]
        folder = os.path.join("test_parent", "test_dst_folder")
        os.mkdir(folder)
        publish_obj = PublishOptions(FIGS_AND_IDS, SRC_DIR, DST_PATH)

        publish_obj.export_imports(os.path.join("tests", "test_publish.py"), folder)

        file_path = os.path.join(folder, "required_imports.txt")
        assert os.path.isfile(file_path)
        with open(file_path, "r", encoding="utf-8") as file:
            modules = file.readlines()
        print(modules, expected_modules)
        self.assertEqual(
            Counter(modules),
            Counter(expected_modules),
            msg=f"{modules}, {expected_modules}",
        )

    def test_find_plotid_calls(self) -> None:
        """Test if all calls to plotID in a file are found."""
        find_plotid_calls(PYTHON_FILE, DST_DIR)
        copied_file = os.path.join(DST_DIR, PYTHON_FILE)
        expected = (
            "# This script was automatically processed by plotID to comment "
            "all\n# function calls to plotID.\nimport sys\n# from plotid.tagplot import"
            " tagplot\n# import plotid\nx=123\ns='abc'\n# publish(\n# 'Lorem ipsum',"
            "\n# x+1 (\n# )  )  \n# tagplot()\n \n\n\n# tagplot(()) \nsys.exit()"
        )
        with open(copied_file, "r", encoding="utf-8") as file:
            new_content = file.read()
        self.assertEqual(new_content, expected)

    def test_find_pattern(self) -> None:
        """Test if RegEx pattern is found and correct list of lines is returned."""
        pattern_simple = re.compile(r"incidunt")
        pattern_bracket = re.compile(r"ipsum\(")
        lines_simple = find_pattern(TEXT_FILE, pattern_simple)
        self.assertEqual(lines_simple, [4])
        lines_bracket = find_pattern(TEXT_FILE, pattern_bracket)
        self.assertEqual(lines_bracket, [0, 1, 2, 3])

    def test_comment_lines(self) -> None:
        """Test if correct lines get commented."""
        expected = (
            "# This script was automatically processed by plotID to comment "
            "all\n# function calls to plotID.\n"
            "Lorem ipsum(\n# dolor\nsit() amet(,\n# consectetur) adipisici )elit, sed"
            " eiusmod tempor\nincidunt ut\nlab\n# ore et dolore\nmagna aliqua."
        )
        comment_lines(TEXT_FILE, {1, 3, 6}, DST_DIR)
        with open(os.path.join(DST_DIR, TEXT_FILE), "r", encoding="utf-8") as file:
            new_content = file.read()
        self.assertEqual(new_content, expected)

    def tearDown(self) -> None:
        """Delete all files created in setUp."""
        shutil.rmtree(SRC_DIR)
        shutil.rmtree(DST_PARENT_DIR)
        shutil.rmtree(DST_DIR)
        os.remove(TEXT_FILE)
        os.remove(PYTHON_FILE)
        for file in SRC_FILES:
            os.remove(file)


if __name__ == "__main__":
    unittest.main()
