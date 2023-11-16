autoload -Uz vcs_info
precmd() { vcs_info }

zstyle ':vcs_info:git:*' formats '%b '

setopt PROMPT_SUBST
PROMPT='%F{green}%n%f%F{white}@%f%F{cyan}%m%f %F{blue}%~%f %F{red}${vcs_info_msg_0_}%f$ '

[[ -r ~/.repos/znap/znap.zsh ]] ||
	git clone --depth 1 -- https://github.com/marlonrichert/zsh-snap.git ~/.repos/znap
source ~/.repos/znap/znap.zsh
znap source marlonrichert/zsh-autocomplete

