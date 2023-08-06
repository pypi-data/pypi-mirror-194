#include <petsc/private/taoimpl.h> /*I "petsctao.h" I*/

/*@C
   TaoPythonSetType - Initialize a Tao object implemented in Python.

   Collective

   Input Parameters:
+  tao - the optimation solver (Tao) context.
-  pyname - full dotted Python name [package].module[.{class|function}]

   Options Database Key:
.  -tao_python_type <pyname> - python class

   Level: intermediate

.seealso: `TaoCreate()`, `TaoSetType()`, `TAOPYTHON`, `PetscPythonInitialize()`
@*/
PetscErrorCode TaoPythonSetType(Tao tao, const char pyname[])
{
  PetscFunctionBegin;
  PetscValidHeaderSpecific(tao, TAO_CLASSID, 1);
  PetscValidCharPointer(pyname, 2);
  PetscTryMethod(tao, "TaoPythonSetType_C", (Tao, const char[]), (tao, pyname));
  PetscFunctionReturn(0);
}

/*@C
   TaoPythonGetType - Get the type of a Tao object implemented in Python.

   Not collective

   Input Parameter:
.  tao - the optimation solver (Tao) context.

   Output Parameter:
.  pyname - full dotted Python name [package].module[.{class|function}]

   Level: intermediate

.seealso: `TaoCreate()`, `TaoSetType()`, `TaoPYTHON`, `PetscPythonInitialize()`, `TaoPythonSetType()`
@*/
PetscErrorCode TaoPythonGetType(Tao tao, const char *pyname[])
{
  PetscFunctionBegin;
  PetscValidHeaderSpecific(tao, TAO_CLASSID, 1);
  PetscValidPointer(pyname, 2);
  PetscUseMethod(tao, "TaoPythonGetType_C", (Tao, const char *[]), (tao, pyname));
  PetscFunctionReturn(0);
}
