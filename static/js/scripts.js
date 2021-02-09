var board = ChessBoard('myBoard', {
    position: 'start',
    draggable: true,
    onDrop: onDrop
});


function get_square(sq) {
    var files = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7};

    return 8*(parseInt(sq.charAt(1)) - 1) + files[sq.charAt(0)];
}

function onDrop(source, target, piece) {
    if(source == target) return

    var promotion = piece.toLowerCase().charAt(1) == 'p' && parseInt(target.charAt(1)) == 8;

    $.get('/move_coordinates', {'from': get_square(source), 'to': get_square(target), 'promotion': promotion}, function(r) {
    if (r.includes("game over")) {
        document.querySelector('p').innerText = 'game over';
    } 
    else {
        document.querySelector('p').innerText = '';
        board.position(r);
    }
    });
}

/*
function newGame() {
    $.get('/newgame', function(r) {
    document.querySelector('p').innerText = '';
    board.position(r);
    });
}
*/
