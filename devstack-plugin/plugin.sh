#!/bin/bash

function install_vm_cost_audit {
    echo "==> Installazione script vm_cost_estimator.py"
    chmod +x $DEST/vm_cost_audit/vm_cost_estimator.py
}

if is_service_enabled vm_cost_audit; then
    case $1 in
        install)
            install_vm_cost_audit
            ;;
    esac
fi