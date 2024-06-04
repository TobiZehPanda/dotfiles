autoload -Uz vcs_info
precmd() { vcs_info }

zstyle ':vcs_info:git:*' formats '%b '

setopt PROMPT_SUBST
PROMPT='%(!.%F{red}.%F{green})%n%f%F{white}@%f%F{cyan}%m%f %F{blue}%~%f %F{red}${vcs_info_msg_0_}%f$ '

[[ -r ~/.repos/znap/znap.zsh ]] ||
	git clone --depth 1 -- https://github.com/marlonrichert/zsh-snap.git ~/.repos/znap
source ~/.repos/znap/znap.zsh
znap source marlonrichert/zsh-autocomplete

export PATH=$HOME/.local/share/gem/ruby/3.0.0/bin:$PATH
export EDITOR=vim
export PF_ASCII="Catppuccin"
export PF_COL3=1
export PASTEL_COLOR_MODE=24bit
export QT_QPA_PLATFORMTHEME=gtk2

alias ls='ls --color=auto'
alias grep='grep --color'
alias ip='ip -color=auto'
alias public_ip='curl --ipv4 ifconfig.me'
alias aria2c='aria2c -s16 -x16'
alias tb="nc termbin.com 9999"

source ~/.zsh/catppuccin_mocha-zsh-syntax-highlighting.zsh
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

bindkey -v
bindkey ^R history-incremental-search-backward
bindkey ^S history-incremental-search-forward

#History
export HISTFILE=~/.histfile
export HISTFILESIZE=1000000
export HISTSIZE=1000000
export SAVEHIST=1000000
setopt appendhistory
