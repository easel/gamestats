CANDLE="$(WIX_HOME)/candle.exe"
LIGHT="$(WIX_HOME)/light.exe"
DOXYGEN="$(DOXYGEN_HOME)/bin/doxygen.exe"
HHC="$(HHC_HOME)/hhc.exe"
ISCC="$(INNOSETUP_HOME)/iscc" 
GFIX="$(FIREBIRD_HOME)/bin/gfix.exe"
ISQL="$(FIREBIRD_HOME)/bin/isql.exe"
GBAK="$(FIREBIRD_HOME)/bin/gbak.exe"
DCC="$(DELPHI_HOME)/bin/dcc32.exe"
FPC="$(FPC_HOME)/bin/win32/fpc.exe" 
DEVENV="$(DEVENV_HOME)/devenv"
INCLUDES="-U$(DELPHI_HOME)\lib" -U$(BPL_DIR)
FPC_INCLUDES=
# -$L+
#DCC_FLAGS=$(INCLUDES) -GD -$$D- -$$R- -$$I- -$$O+
DCC_FLAGS=$(INCLUDES) "-GD" "-\$D- -\$R- -\$I- -\$O+"
#DCC_FLAGS=$(INCLUDES)
FPC_FLAGS=$(FPC_INCLUDES)
#DCC_FLAGS=$(FPC_FLAGS)
PYTHON="$(PYTHON_HOME)/python.exe"
SVN="$(SUBVERSION_HOME)/bin/svn.exe"
COPY=cmd /c copy
DEL=cmd /c del
DELDIR=rm -rf
REN=cmd /c ren

MSM_DIR=$(prefix)/deploy
DLL_DIR=$(prefix)/devdll
export BPL_DIR="$(DELPHI_HOME)\Projects\BPL"
THIS_FILE=$(wordlist $(words $(MAKEFILE_LIST)), \
	$(words $(MAKEFILE_LIST)), $(MAKEFILE_LIST))
REGISTER_DPK=$(PYTHON) $(subst interlink.mk,register_dpk.py, $(THIS_FILE))
UNZIP=$(subst interlink.mk,unzip.exe, $(THIS_FILE))

$(MSM_DIR)/%.msm:	%.msm
	$(COPY) $< $@

$(DLL_DIR)/%.dll:	%.dll
	$(COPY) $< $@

%.zcb 	: 	%.fbk
	$(DEL) $@
	bzip2 $<
	$(REN) $<.bz2 $@

%.fbk 	: 	%.fdb
	$(GBAK) $< -B $@

%.fdb 	: 	%.sql
	$(DEL) $@
	$(ISQL) -s 3 -i $<
	$(REN) $@ $@

%.res 	: 	%.rc
	brcc32 $<

%.wixobj : 	%.wxs
	candle $<

%.msi	:	%.wixobj
	light $<

%.msm 	:	%.wixobj
	light $<

%	: 	%.zip
	rm -rf $@
	$(UNZIP) $@.zip -d $@


%.dcp %.bpl:	%.dpk
	$(DCC) $(DCC_FLAGS) -LE. -LN. $<
	$(COPY) $@ $*.dcp $(BPL_DIR)
	$(REGISTER_DPK) $<
