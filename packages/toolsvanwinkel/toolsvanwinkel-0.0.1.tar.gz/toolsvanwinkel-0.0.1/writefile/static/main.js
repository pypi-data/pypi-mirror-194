define([
  'base/js/namespace',
  'base/js/dialog',
  'jquery',
], function(Jupyter, dialog, $) {

  function write() {
    var cell_list = []
    var all_files = {}

    var cells = Jupyter.notebook.get_cells();
    var start = 0;
    for (var cell of cells) {
        var cell_text = cell.get_text()
        if (cell_text.substring(0,8) == "#INCLUDE") {
           splitted_text = cell_text.split(/\r?\n/)
           var filename = splitted_text[0].substring(9)
           if (filename in all_files) {
             all_files[filename].push(splitted_text.slice(1).join('\n'))
           }
           else {
             all_files[filename] = [splitted_text.slice(1).join('\n')]
           }
           //cell_list.push(cell_text.substring(10))
        }
    }

   //console.log(all_files)
   for (var filename in all_files) {
     command = '%%writefile ' + $.trim(filename) + '\n' + all_files[filename].join('\n\n');
     var kernel = IPython.notebook.kernel;
     kernel.execute(command);
   }

    //var textarea = $('<textarea/>')
    //    .attr('rows','1')
    //    .attr('cols','80')
    //    .attr('name','cell_name');

    //var dialogform = $('<div/>')
    //    .append(
    //        $('<form/>').append(
    //            $('<fieldset/>').append(
    //                $('<label/>')
    //                .attr('for','cell_name')
    //                .text("A new file with your selected cell content" +
    //                "will be created after you name the file.")
    //                )
    //                .append($('<br/>'))
    //                .append(
    //                    textarea
    //                )
    //            )
    //    );

    //dialog.modal({
    //    title: "Create a file with your cell content",
    //    body: dialogform,
    //    keyboard_manager: Jupyter.keyboard_manager,
    //    buttons: {
    //            "OK": { class : "btn-primary",
    //                click: function() {

                      //command = '%%writefile ' + $.trim($(textarea).val()) + '\n' + cell_list.join('\n\n');
                      //var kernel = IPython.notebook.kernel;
                      //kernel.execute(command);
    //            }},
    //    Cancel: {}
    //        }
    //});

  }

  var write_file = function() {
    Jupyter.toolbar.add_buttons_group([
      Jupyter.keyboard_manager.actions.register ({
        'help': 'Write to file',
        'icon': 'fa-file',
        'handler': function(){write();}
      }, 'write')
    ]);
  };

  var extension = {
     load_ipython_extension: write_file
  };

  return  extension;
}
);
