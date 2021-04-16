
(defpackage :chrysalis (:use :cl))

(defun start-gui ()
  (format t "Starting gui..."))

(defun main ()
  (let ((v "0.0.1"))
   (format t "Chrysalis v~$~%" v))
  (start-gui))

