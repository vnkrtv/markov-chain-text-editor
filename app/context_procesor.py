import flask


def save_icon_path():
    def save_icon():
        return flask.url_for('static', filename='images/icons/save.svg')
    return dict(save_icon=save_icon)


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


def user_icon_path():
    def user_icon():
        return flask.url_for('static', filename='images/icons/user.svg')
    return dict(user_icon=user_icon)


def add_doc_icon_path():
    def add_doc_icon():
        return flask.url_for('static', filename='images/icons/add_doc.svg')
    return dict(add_doc_icon=add_doc_icon)


def add_icon_path():
    def add_icon():
        return flask.url_for('static', filename='images/icons/add.svg')
    return dict(add_icon=add_icon)


def gears_icon_path():
    def gears_icon():
        return flask.url_for('static', filename='images/icons/gears.svg')
    return dict(gears_icon=gears_icon)
