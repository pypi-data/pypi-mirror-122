from gorp.test import test_ku_options
from gorp.test import test_jsonpath
from gorp.test import test_textcache
from gorp.test import test_option_combos
from gorp.test import test_pdf_option
from gorp.test import test_q_option
import doctest

def main():
    print("WARNING: If you put any files into testDir other than what's in there by default, some of the tests are likely to fail.")
    print("===============\nTesting TextCache")
    tc = test_textcache.main()
    print("===============\nTesting killing and updating of files")
    test_ku_options.main()
    print("===============\nTesting jsonpath (no output means everything is fine)")
    doctest.testmod(test_jsonpath)
    print("===============\nTesting many different combinations of options")
    test_option_combos.test_combo_results()
    print("===============\nTesting the PDF option")
    test_pdf_option.main()
    print("===============\nTesting the q option for unioning resultsets")
    test_q_option.main()
    
if __name__ == '__main__':
    main()