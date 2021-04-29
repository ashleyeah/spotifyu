$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#album-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes
        const date = button.data('date')

        const modal = $(this)
        if (taskID === 'New Album') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Album Name')
            $('#task-form-display').attr('taskID', taskID)
        }

        if (content) {
            modal.find('#album_name').val(content);
            modal.find('#album_id').val(taskID);
            modal.find('#release_date').val(date);
        } else {
            modal.find('.form-control').val('');
        }
    })

    $('#submit-album').click(function () {
        const tID = $('#task-form-display').attr('taskID');
        console.log($('#album-modal').find('.form-control').val()) //prints out song name from .form-control
        $.ajax({
            type: 'POST',
            url: tID ? '/album/edit/' + tID : '/album/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'id': $('#album_id').val(),
                'name': $('#album_name').val(), //puts the song name into data['description']
                'date': $('#release_date').val()
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.remove-album').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/album/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    }); 

    $('#artist-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes

        const modal = $(this)
        if (taskID === 'New Artist') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Artists Name')
            $('#task-form-display').attr('artistID', taskID)
        }

        if (content) {
            modal.find('#artist_name').val(content);
            modal.find('#artist_id').val(taskID);
        } else {
            modal.find('.form-control').val('');
        }
    })

    $('#submit-artist').click(function () {
        const tID = $('#task-form-display').attr('taskID');
        console.log(tID);
        console.log($('#artist-modal').find('.form-control').val()) //prints out song name from .form-control
        $.ajax({
            type: 'POST',
            url: tID ? '/artist/edit/' + tID : '/artist/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'id': $('#artist_id').val(),
                'name': $('#artist_name').val() //puts the song name into data['description']
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.remove-artist').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/artist/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

});