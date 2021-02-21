from lektor_youtube_embed import _get_youtube_id, _youtube


def test_get_youtube_id_valid_formats():
    urls = [
        "http://www.youtube.com/watch?v=KIGXGkzjAoc",
        "http://www.youtube.com/watch?v=KIGXGkzjAoc#t=0m10s",
        "http://www.youtube.com/watch?v=KIGXGkzjAoc&foo=bar",
        "http://www.youtube.com/embed/KIGXGkzjAoc",
        "http://www.youtube.com/embed/KIGXGkzjAoc#t=0m10s",
        "http://www.youtube.com/embed/KIGXGkzjAoc?foo=bar",
        "http://youtu.be/KIGXGkzjAoc",
        "http://youtu.be/KIGXGkzjAoc#t=0m10s",
        "http://youtu.be/KIGXGkzjAoc?foo=bar",
    ]
    for url in urls:
        assert _get_youtube_id(url) == "KIGXGkzjAoc"


def test_get_youtube_id_invalid_formats():
    urls = [
        "",
        "http://youtu.be/",
        "http://www.youtube.com/",
        "https://www.youtube.com/user/PewDiePie?gl=GB",
        "https://www.google.com/",
        "foobar",
    ]
    for url in urls:
        assert _get_youtube_id(url) is None


def test_youtube_no_params():
    expected = (
        '<iframe src="https://www.youtube.com/embed/KIGXGkzjAoc"\n'
        + '  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"\n'
        + '  frameborder="0" allowfullscreen ></iframe>\n'
    )
    assert _youtube("http://www.youtube.com/watch?v=KIGXGkzjAoc") == expected


def test_youtube_with_params():
    expected = (
        '<iframe width="640" height="480" src="https://www.youtube.com/embed/KIGXGkzjAoc"\n'
        + '  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"\n'
        + '  frameborder="0" allowfullscreen id="youtube-iframe" class="video"></iframe>\n'
    )
    assert (
        _youtube(
            "http://www.youtube.com/watch?v=KIGXGkzjAoc",
            width=640,
            height=480,
            attrs={"id": "youtube-iframe", "class": "video"},
        )
        == expected
    )


def test_youtube_invalid_input():
    assert _youtube("foobar") == "foobar"


def test_youtube_escaping():
    assert "<script>" not in _youtube(
        "http://www.youtube.com/watch?v=<script>alert('XSS');</script>",
        width="<script>alert('XSS');</script>",
        height="<script>alert('XSS');</script>",
        attrs={"<script>alert('XSS');</script>": "<script>alert('XSS');</script>"},
    )
