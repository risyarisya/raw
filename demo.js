$.fn.wPaint.extend({
	getImageCanvas: function (withBg) { // getCanvas is bad name (conflict).
	    var canvasSave = document.createElement('canvas'),
		ctxSave = canvasSave.getContext('2d');

	    withBg = withBg === false ? false : true;

	    $(canvasSave)
		.css({display: 'none', position: 'absolute', left: 0, top: 0})
		.attr('width', this.width)
		.attr('height', this.height);

	    if (withBg) { ctxSave.drawImage(this.canvasBg, 0, 0); }
	    ctxSave.drawImage(this.canvas, 0, 0);

	    return canvasSave;
	}
});

$(function() {
	//	$('#img_pane').show();

	$('#load_org_file').on('change', function(e) {
	    console.log("in!");
	    var file = e.target.files[0];
	    if (file.type.indexOf('image') < 0) {
		return false;
	    }
	    set_file(file);
	});
	$('#background').load(function() {
	    $('#wPaint')
		.width($('#background').width())
		.height($('#background').height())
		.wPaint('resize');
	    var wPaintOuterWidth = $('#wPaint').outerWidth(true);
	    $('#img_pane .span6').width(wPaintOuterWidth);
	    $('#img_pane').width(wPaintOuterWidth * 2 + 30);
	    colorize(10);
	});

	$('#submit').click(function() {
	    console.log("submit!");
	    colorize(10);
	});

	function blobUrlToBlob(url, fn) {
	    var xhr = new XMLHttpRequest();
	    xhr.onload = function () {
		fn(xhr.response);
	    };
	    xhr.open('GET', url);
	    xhr.responseType = 'blob';
	    xhr.send();
	}

	function post(data) {
	    $.ajax({
		type: 'POST',
		url: 'http://0.0.0.0:8000/cgi-bin/save.py',
		data: data,
		cache: false,
		contentType: false,
		processData: false,
		dataType: 'text',
		success: function() {
			console.log('OK');
		}
	    });
	}

	function colorize(new_image_id) {

	    $('#wPaint').wPaint('imageCanvas').toBlob(function(result) {
		var ajaxData = new FormData();
		ajaxData.append('ref', result);
		ajaxData.append('id', "10");
		blobUrlToBlob($('#background').attr('src'), function(result2) {
		    ajaxData.append('back', result2);
		    post(ajaxData);
		});
	    });
	}

	function resetOrigin() {
	    if (location.hostname === '0.0.0.0') {
		if (location.protocol === 'http:') {
		    origin = '//0.0.0.0:8000';
		}
	    }
	}

	function set_file(file) {
	    console.log(file);
	    $('#img_pane').show('fast', function() {
		    $('#background').attr('src', window.URL.createObjectURL(file));
	    });
	};
});
	    