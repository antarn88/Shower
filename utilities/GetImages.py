from PySide2.QtCore import QByteArray
from PySide2.QtGui import QPixmap


def app_icon():
    base64data = b"iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAADOUlEQVRoge1Zz08TURD+5m2BKL1oYiRg5QRSmxCNbSKREqrhRAXUwIGDN9CLBy" \
                 b"/+DXIx8WLScMfEBAKGiJHwm2JMaqIoBCIasWAKF0g0mFK640HQ7rb8eNtdW0i/ZA9v9s3M9" \
                 b"/XNe7O7JZiIvsm5c0RqEwh1AJcA5Phzh8MALYMxyCx6G6sr5s3KSWYE6Zucc5PgDoCvHjDplEriQWNVRTDd3GkJCIRCecXR44+ZcNdALGbgSSR/4/4dtztmlINhAS" \
                 b"+nZk5ugroB1BqNAQBEPEJb8Vt+b+WaEX9hxCkQCuXtQf4VEdpYFRUFhTF7QWHMTlCcxNQOxqB+MjP52KZ0B0KhPCNcbEactsumVmeeFyq3+atdEylc5ravzr7gbA2ATiKU79xkJl" \
                 b"/x5rFHAO7JcpEuoefBjx6QeKPzHYtHo003fBfXDxKjf2L6hKrYegHUJJhZCPL4LzvfyvCRLiES1AEt+XkZ8gDg91auifhWE4BPiaFZ5YfSfGQm97" \
                 b"/+4FRZmdUEIPJdr3KOyiYGgL7gbA0RxhJtrIoKmT4htQKqqjRoDIxBo+QBoPHK" \
                 b"+XEAQxpCQm3YZXpKyJUQoU4zFHgm5Z86qCYGszbHfpASwAxH4liNi1QnjhQIYlxnOCvjLyWACMWJ42gsvizjnwq/oltLOlOJjL/sKWRPHLT4XD8l" \
                 b"/ZOQIoY95cRdYKgTZxOkOvFq5LslJNKJm9QHtmZRz4wAS9ai1SBgiYB2mwsDOrsWsRmEGTjz/6hJIZzv0p5SSXsgi8kD0B7jwBHYxDkBmcahF5DUB36sZIKGcRz6FTj0Agy91O" \
                 b"+HWJzQNVSK4XenQAB8F1bReu0b8hQ2PZclAp4Ol6Jn8l8/7Jl0gIhwu+6r6bksKaHR6SIIITTXyPsiK1JZswLMCoTQ/jZEihWpkgVsRNIP6i1fwcC09s3QWxYxJbYelqxAs" \
                 b"/szBAEvpksBAPWVi7h56YsVqazZA4pgtHgW/tZ/s2cBijD/BAIsWoEd6PeBFcgJ2Atlp9dBpvwHtDuSwoe7YE2xmgRHq5Zz0gosWvPhwTIc+oe5nIBM4+gJYED" \
                 b"/tTibENYbkgQQ0J6lIsIs0J5pEjnkkG34DXqW5s+fkTdHAAAAAElFTkSuQmCC "

    ba = QByteArray.fromBase64(base64data)
    app_icon_img = QPixmap()
    app_icon_img.loadFromData(ba)
    return app_icon_img
