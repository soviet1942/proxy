import base64
import os
import random
import re
import sys
import redis
import requests

from catcher import redisDB
from config import base

if __name__ == '__main__':
    a = """
    <html>
<head>
<title>▒▒▒▒▒ 차단된 페이지 ▒▒▒▒▒</title>
</head>
<body bgcolor="#FFFFFF" text="#000000" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width="100%%" border="0" cellspacing="0" cellpadding="0" height="100%%">
  <tr>
    <td bgcolor="#E6E6E6" align="center"> 
      <table width="422" border="0" cellspacing="0" cellpadding="0">
        <tr><td><img src="/images/page_e01.gif" width="422" height="60"></td></tr>
        <tr><td><img src="/images/page_e02.gif" width="422" height="36"></td></tr>
        <tr>
          <td background="/images/page_ebg.gif" align="center" bgcolor="#FFFFFF"> 
            <table width="397" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td height="50" align="center" style='font:10pt Georgia;'>
                  <p>&nbsp;</p>
                  <p>요청하신 페이지는 방화벽에 의해서 차단되었습니다.</p>
                  <p>관리자에게 문의 부탁 드립니다.</p>
                  <p>&nbsp;</p>
                </td>
              </tr>
              <tr>
                <td height="40" align="left" style='font:9pt Georgia;color=blue'>
                  <p>※ 웹 브라우저 캐쉬 문제로 요청하신 페이지가 차단될 경우가 있습니다.<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;이때 모든 웹 브라우저를 종료한 다음에 다시 실행하시기 바랍니다.</p>
                </td>
              </tr>
            </table>
            <table width="397" border="0" cellspacing="0" cellpadding="0">
              <tr><td height="7" align="center"></td></tr>
              <tr><td height="7" align="center"></td></tr>
            </table>
          </td>
        </tr>
        <tr><td><img src="/images/page_e03.gif" width="422" height="23"></td></tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>
    """
    print(a.find("table"))