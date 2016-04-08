KindEditor.ready(function(K) {
        //window.editor = K.create('#editor_id');
    K.create('textarea[name=content]', {
        width: '500px',
        height: '500px',
        uploadJson: '/admin/upload/kindeditor',
    });
});