import flask


def close_icon_path():
    def close_icon():
        return flask.url_for('static', filename='images/icons/close.svg')
    return dict(close_icon=close_icon)


def sort_icon_path():
    def sort_icon():
        return flask.url_for('static', filename='images/icons/sort-solid.svg')
    return dict(sort_icon=sort_icon)


def delete_icon_path():
    def delete_icon():
        return flask.url_for('static', filename='images/icons/trash.svg')
    return dict(delete_icon=delete_icon)


def update_icon_path():
    def update_icon():
        return flask.url_for('static', filename='images/icons/update.svg')
    return dict(update_icon=update_icon)
