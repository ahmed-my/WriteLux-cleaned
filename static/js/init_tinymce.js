document.addEventListener('DOMContentLoaded', function() {
    tinymce.init({
        selector: 'textarea.tinymce',
        height: 360,
        width: 800,
        cleanup_on_startup: true,
        custom_undo_redo_levels: 20,
        theme: 'modern',
        plugins: 'textcolor save link image media preview codesample contextmenu table code lists fullscreen insertdatetime nonbreaking contextmenu directionality searchreplace wordcount visualblocks visualchars code fullscreen autolink lists charmap print hr anchor pagebreak',
        toolbar1: 'fullscreen preview bold italic underline | fontselect fontsizeselect | forecolor backcolor | alignleft alignright | aligncenter alignjustify | indent outdent | bullist numlist table | link image media | codesample',
        toolbar2: 'visualblocks visualchars | charmap hr pagebreak nonbreaking anchor | code | save | contextmenu searchreplace wordcount | insertdatetime media',
        directionality: 'ltr',
        strict_loading_mode: 1
    });
});
