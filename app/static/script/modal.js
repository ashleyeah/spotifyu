$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    
    
    /***********************************************
    *                 Album Modal                  *
    *                                              *
    ***********************************************/
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


    /***********************************************
    *                 Artist Modal                 *
    *                                              *
    ***********************************************/
    $('#artist-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes

        const modal = $(this)
        console.log(taskID)
        if (taskID === 'New Artist') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Artists Name')
            $('#task-form-display').attr('taskID', taskID)
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
        //console.log(tID); if this is NULL, do create
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


    /***********************************************
    *                 Song Modal                   *
    *                                              *
    ***********************************************/
    $('#song-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // source = song_id
        const content = button.data('content') // content = song_name
        const albumContent = button.data('album') // album = album_id
        const modal = $(this)
        console.log("outside if statement")
        if (taskID === 'New Song') {
            modal.find('.modal-title').text(taskID)
            console.log("got in here")
            console.log(modal.find('.modal-title').text(taskID))
            $('#task-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Song Name')
            $('#task-form-display').attr('taskID', taskID)
        }

        if (content) {
            modal.find('#song_name').val(content);
            modal.find('#song_id').val(taskID);
            modal.find('#album_id').val(albumContent);
        } else {
            modal.find('.form-control').val('');
        }
    })


    $('#submit-song').click(function () {
        const tID = $('#task-form-display').attr('taskID');
        console.log(tID)
        console.log($('#task-modal').find('.form-control').val()) //prints out song name from .form-control
        $.ajax({
            type: 'POST',
            url: tID ? '/song/edit/' + tID : '/song/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'song_name': $('#song_name').val(),
                'song_id': $('#song_id').val(), //puts the song name into data['description']
                'album_id': $('#album_id').val()
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

    $('.remove-song').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/song/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });


    /***********************************************
    *                 Genre Modal                   *
    *                                              *
    ***********************************************/
    $('#task-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes

        const modal = $(this)
        if (taskID === 'New Genre') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit the name of the genre')
            $('#task-form-display').attr('taskID', taskID)
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    })


    $('#submit-task').click(function () {
        const tID = $('#task-form-display').attr('taskID');
        console.log($('#task-modal').find('.form-control').val())
        $.ajax({
            type: 'POST',
            url: tID ? '/genre/edit/' + tID : '/genre/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'name': $('#task-modal').find('.form-control').val()
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


    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/genre/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.a').click(function () {
        const link = $(this)
        $.ajax({
            type: 'POST',
            url: '/genre/delete/' + link.data('source'),
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