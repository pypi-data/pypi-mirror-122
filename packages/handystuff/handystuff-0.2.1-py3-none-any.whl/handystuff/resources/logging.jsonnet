local ifh = {
                class: "handystuff.logs.MakeFileHandler",
                level: "INFO",
                formatter: "simple",
                filename: "logs/info.log",
                maxBytes: 10485760,
                backupCount: 20,
                encoding: "utf8",
              };
{
    version: 1,
    formatters: {
      simple: {format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
      colored: {
        log_colors : {
          "DEBUG": "thin_white",
          "INFO": "white",
          "WARNING": "yellow",
          "ERROR": "bold_red",
          "CRITICAL": "bold_red,bg_bold_yellow",
        },
        secondary_log_colors : {
          "message": {
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red",
          }
        },
        format: "%(cyan)s%(asctime)s%(reset)s %(log_color)s%(levelname)-8s%(reset)s %(bold_blue)s%(fqn)-35s%(reset)s %(message_log_color)s%(message)s",
        "()": "colorlog.ColoredFormatter"
      },
    },
    disable_existing_loggers: false,
    root: {
      level: "DEBUG",
      handlers: [
        "console",
        "info_file_handler",
        "error_file_handler",
        "debug_file_handler"
      ]
    },
    filters: {
        fqn_filter: {
          "()": "handystuff.logs.FQNFilter",
          max_len: 35
        }
    },

    handlers: {
      console: {
        class: "handystuff.logs.TQDMHandler",
        level: "DEBUG",
        formatter: "colored",
        filters: ["fqn_filter"],
        stream: "ext://sys.stdout",
      },
      info_file_handler: ifh,
      debug_file_handler: ifh {
        "level": "DEBUG",
        "filename": "logs/debug.log",

      },
      error_file_handler: ifh {
        "filename": "logs/errors.log",
        "level": "ERROR"
      }
    },
    loggers: {
          # here you can change the verbosity of different modules
          parso: {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": false
          },
    }
}

