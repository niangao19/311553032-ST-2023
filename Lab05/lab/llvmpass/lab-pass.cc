/*
  Ref:
  * https://llvm.org/doxygen/
  * https://llvm.org/docs/GettingStarted.html
  * https://llvm.org/docs/WritingAnLLVMPass.html
  * https://llvm.org/docs/ProgrammersManual.html
 */
#include "lab-pass.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/IRBuilder.h"
#include <stdio.h>

using namespace llvm;

char LabPass::ID = 0;

bool LabPass::doInitialization(Module &M) {
  return true;
}

static void dumpIR(Function &F)
{
  for (auto &BB : F) {
    errs() << "BB: " << "\n";
    errs() << BB << "\n";
  }
}

static Constant* getI8StrVal(Module &M, char const *str, Twine const &name) {
  LLVMContext &ctx = M.getContext();

  Constant *strConstant = ConstantDataArray::getString(ctx, str);

  GlobalVariable *gvStr = new GlobalVariable(M, strConstant->getType(), true,
    GlobalValue::InternalLinkage, strConstant, name);

  Constant *zero = Constant::getNullValue(IntegerType::getInt32Ty(ctx));
  Constant *indices[] = { zero, zero };
  Constant *strVal = ConstantExpr::getGetElementPtr(Type::getInt8PtrTy(ctx),
    gvStr, indices, true);

  return strVal;
}

static FunctionCallee printfPrototype_1(Module &M) {
  LLVMContext &ctx = M.getContext();

  FunctionType *printfType = FunctionType::get(
    Type::getInt32Ty(ctx),
    { Type::getInt8PtrTy(ctx) },
    true);

  FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);

  return printfCallee;
}

static FunctionCallee printfPrototype_2(Module &M) {
  LLVMContext &ctx = M.getContext();

  FunctionType *printfType = FunctionType::get(
    Type::getInt32Ty(ctx),
    { Type::getInt8PtrTy(ctx),  Type::getInt32Ty(ctx), Type::getInt8PtrTy(ctx)},
    true);

  FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);

  return printfCallee;
}

static FunctionCallee printfPrototype_3(Module &M) {
  LLVMContext &ctx = M.getContext();

  FunctionType *printfType = FunctionType::get(
    Type::getInt32Ty(ctx),
    { Type::getInt8PtrTy(ctx),  Type::getInt8PtrTy(ctx)}, //,Type::getInt32Ty(ctx)},
    true);

  FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);

  return printfCallee;
}


bool LabPass::runOnModule(Module &M) {
  errs() << "runOnModule\n";

  LLVMContext &ctx = M.getContext();
  FunctionCallee printfCallee = printfPrototype_1(M);
  FunctionCallee printfSpace = printfPrototype_2(M);
  FunctionCallee printfAddr = printfPrototype_3(M);
  // 製造出 0,1
  Constant *zero = Constant::getNullValue(IntegerType::getInt32Ty(ctx));
  Constant *one = Constant::getIntegerValue(Type::getInt32Ty(ctx), APInt(32, 1));
  
  GlobalVariable *globalVar = new GlobalVariable(M, Type::getInt32Ty(ctx), false, GlobalValue::ExternalLinkage, zero, "myGlobalVar");
  //globalVar->getInitializer();

  for (auto &F : M) {
    if (F.empty()) {
      continue;
    }
    errs() << F.getName() << "\n";
    //errs() << *globalVar << "\n";

    // 開始玩 basic block
    BasicBlock &Bstart = F.front();
    BasicBlock &Bend = F.back();
    Instruction &Istart = Bstart.front();
    Instruction &Iend = Bend.back();

    IRBuilder<> BuilderTest(&Istart);

    int32_t intValue = 0;

    //Value *currentValue = globalVar->getInitializer();
    Value *currentValue = BuilderTest.CreateLoad(Type::getInt32Ty(ctx), globalVar, "myGlobalVar");

    // add depth
    if(F.getName() != "main"){
      Constant *space = getI8StrVal(M, " ", "space");
      Constant *format = getI8StrVal(M, "%*s", "format");
      BuilderTest.CreateCall(printfSpace, { format, currentValue, space });
    }

    Constant *stackBofMsg = getI8StrVal(M, F.getName().data(), "stackBofMsg");
    BuilderTest.CreateCall(printfCallee, { stackBofMsg });
    stackBofMsg = getI8StrVal(M, ": ", "stackBofMsg");
    BuilderTest.CreateCall(printfCallee, { stackBofMsg });

    // 輸出地址
    Value* FuncPtr = ConstantExpr::getBitCast(&F, Type::getInt32PtrTy(ctx));
    Constant *format = getI8StrVal(M, "%p", "format");
    BuilderTest.CreateCall(printfAddr, { format, FuncPtr});


    stackBofMsg = getI8StrVal(M, "\n", "stackBofMsg");
    BuilderTest.CreateCall(printfCallee, { stackBofMsg });

    //儲存depth
    Value *newValue = BuilderTest.CreateAdd(currentValue, one);
    BuilderTest.CreateStore(newValue, globalVar);

    //中間有其他 bb，例如呼叫其他 function

    //在最終指令的地方，將depth加回
    IRBuilder<> BuilderEnd(&Iend);
    currentValue = BuilderEnd.CreateLoad(Type::getInt32Ty(ctx), globalVar, "myGlobalVar");
    newValue = BuilderEnd.CreateSub(currentValue, one);
    BuilderEnd.CreateStore(newValue, globalVar);

  }
  return true;
}

static RegisterPass<LabPass> X("labpass", "Lab Pass", false, false);
